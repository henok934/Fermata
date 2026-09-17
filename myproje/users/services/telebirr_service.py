import base64
import io
import json
import logging
import os
import re
import secrets
import time
import urllib.parse
from typing import Any, Optional

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from django.conf import settings
import httpx
import qrcode

logger = logging.getLogger(__name__)

EXCLUDE_FIELDS = {
    "sign",
    "sign_type",
    "header",
    "refund_info",
    "openType",
    "raw_request",
    "wallet_reference_data",
}


def _wrap_pem(clean: str, label: str) -> str:
    lines = [clean[i : i + 64] for i in range(0, len(clean), 64)]
    return f"-----BEGIN {label}-----\n" + "\n".join(lines) + f"\n-----END {label}-----"


def _load_private_key(key: str) -> RSAPrivateKey:
    if not key:
        raise ValueError("TELEBIRR_PRIVATE_KEY አልተገኘም!")
    clean_key = str(key).strip().strip('"').strip("'").replace("\\n", "\n")
    if "BEGIN" in clean_key:
        pem = clean_key
    else:
        clean = "".join(clean_key.split())
        pem = _wrap_pem(clean, "PRIVATE KEY")
    try:
        return serialization.load_pem_private_key(pem.encode("utf-8"), password=None)
    except Exception:
        clean = "".join(clean_key.split())
        pem = _wrap_pem(clean, "RSA PRIVATE KEY")
        return serialization.load_pem_private_key(pem.encode("utf-8"), password=None)


def _load_public_key(key: str) -> RSAPublicKey:
    if not key:
        raise ValueError("TELEBIRR_PUBLIC_KEY አልተገኘም!")
    clean_key = str(key).strip().strip('"').strip("'").replace("\\n", "\n")
    if "BEGIN" in clean_key:
        pem = clean_key
    else:
        clean = "".join(clean_key.split())
        pem = _wrap_pem(clean, "PUBLIC KEY")
    return serialization.load_pem_public_key(pem.encode("utf-8"))


def sort_object(obj: Any) -> Any:
    if not isinstance(obj, dict):
        return obj
    return {k: sort_object(obj[k]) for k in sorted(obj.keys())}


def _stringify_no_whitespace(value: Any) -> str:
    return json.dumps(sort_object(value), separators=(",", ":"), ensure_ascii=False)


def build_sign_string(request: dict | str) -> str:
    data = json.loads(request) if isinstance(request, str) else request

    biz_content = data.get("biz_content")
    merged: dict[str, Any] = {}

    for k, v in data.items():
        if k != "biz_content":
            merged[k] = v

    if isinstance(biz_content, dict):
        merged.update(biz_content)
    elif isinstance(biz_content, str):
        try:
            parsed_biz = json.loads(biz_content)
            if isinstance(parsed_biz, dict):
                merged.update(parsed_biz)
        except Exception:
            pass

    parts: list[str] = []
    for key in sorted(merged.keys()):
        if key in EXCLUDE_FIELDS:
            continue
        val = merged[key]
        if val is None or val == "":
            continue
        if isinstance(val, (dict, list)):
            str_val = _stringify_no_whitespace(val)
        elif isinstance(val, bool):
            str_val = "true" if val else "false"
        else:
            str_val = str(val)
        parts.append(f"{key}={str_val}")
    return "&".join(parts)


def sign_payload_rsa_pss(request: dict, private_key_pem: str) -> str:
    sign_str = build_sign_string(request)
    key = _load_private_key(private_key_pem)
    signature = key.sign(
        sign_str.encode("utf-8"),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.DIGEST_LENGTH,
        ),
        hashes.SHA256(),
    )
    return base64.b64encode(signature).decode("ascii")


def verify_sign_rsa(request: dict | str, public_key_pem: str, signature_b64: str) -> bool:
    sign_str = build_sign_string(request)
    key = _load_public_key(public_key_pem)
    try:
        key.verify(
            base64.b64decode(signature_b64),
            sign_str.encode("utf-8"),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.DIGEST_LENGTH,
            ),
            hashes.SHA256(),
        )
        return True
    except (InvalidSignature, ValueError):
        return False


def generate_qr_data_uri(data: str) -> str:
    img = qrcode.make(data, border=2)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    encoded = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def create_nonce_str(length: int = 32) -> str:
    _chars = "0123456789abcdefghijklmnopqrstuvwxyz"
    return "".join(secrets.choice(_chars) for _ in range(length))


class TelebirrService:

    def __init__(
        self,
        out_trade_no: Optional[str] = None,
        total_amount: Optional[float] = None,
        subject: Optional[str] = None,
        notify_url: Optional[str] = None,
        redirect_url: Optional[str] = None,
    ):
        config = getattr(settings, "TELEBIRR_CONFIG", {})

        self.base_url = (
            config.get("TELEBIRR_BASE_URL")
            or config.get("BASE_URL")
            or os.getenv("TELEBIRR_BASE_URL")
            or "https://developerportal.ethiotelebirr.et:38443/apiaccess/payment/gateway"
        ).rstrip("/")

        raw_merch_code = (
            config.get("TELEBIRR_MERCHANT_CODE")
            or config.get("merchantCode")
            or os.getenv("TELEBIRR_MERCHANT_CODE")
            or "259159"
        )
        self.merchant_code = str(raw_merch_code).strip().strip('"').strip("'")

        raw_merch_app_id = (
            config.get("TELEBIRR_MERCHANT_APP_ID")
            or config.get("merchantAppId")
            or os.getenv("TELEBIRR_MERCHANT_APP_ID")
            or "1674185087411200"
        )
        self.merchant_app_id = str(raw_merch_app_id).strip().strip('"').strip("'")

        raw_fabric_id = (
            config.get("TELEBIRR_APP_ID")
            or config.get("fabricAppId")
            or os.getenv("TELEBIRR_APP_ID")
            or "c4182ef8-9249-458a-985e-06d191f4d505"
        )
        self.fabric_app_id = str(raw_fabric_id).strip().strip('"').strip("'")

        raw_app_secret = (
            config.get("TELEBIRR_APP_SECRET")
            or config.get("appSecret")
            or os.getenv("TELEBIRR_APP_SECRET")
            or ""
        )
        self.app_secret = str(raw_app_secret).strip().strip('"').strip("'")

        self.web_base_url = str(
            config.get("TELEBIRR_WEB_BASE_URL")
            or config.get("WEB_BASE_URL")
            or os.getenv("TELEBIRR_WEB_BASE_URL")
            or "https://developerportal.ethiotelebirr.et:38443/payment/web/paygate"
        ).strip().strip('"').strip("'").rstrip("/?")

        self.notify_url = str(
            notify_url
            or config.get("TELEBIRR_NOTIFY_URL")
            or config.get("notify_url")
            or os.getenv("TELEBIRR_NOTIFY_URL")
            or ""
        ).strip().strip('"').strip("'")

        self.redirect_url = str(
            redirect_url
            or config.get("TELEBIRR_REDIRECT_URL")
            or config.get("redirect_url")
            or os.getenv("TELEBIRR_REDIRECT_URL")
            or ""
        ).strip().strip('"').strip("'")

        self.private_key_pem = str(
            config.get("TELEBIRR_PRIVATE_KEY")
            or config.get("PRIVATE_KEY")
            or os.getenv("TELEBIRR_PRIVATE_KEY")
            or ""
        ).strip()

        self.public_key_pem = str(
            config.get("TELEBIRR_PUBLIC_KEY")
            or config.get("PUBLIC_KEY")
            or os.getenv("TELEBIRR_PUBLIC_KEY")
            or ""
        ).strip()

        self.out_trade_no = out_trade_no
        self.total_amount = total_amount
        self.subject = subject
        self._token: Optional[str] = None

    def _get_fabric_token(self) -> Optional[str]:
        if self._token:
            return self._token
        url = f"{self.base_url}/payment/v1/token"
        headers = {
            "Content-Type": "application/json;charset=utf-8",
            "X-APP-Key": self.fabric_app_id,
        }
        payload = {
            "appId": self.fabric_app_id,
            "appSecret": self.app_secret,
        }
        try:
            with httpx.Client(
                verify=False, follow_redirects=True, timeout=15.0
            ) as client:
                res = client.post(url, json=payload, headers=headers)
                res.raise_for_status()
                res_data = res.json()
                self._token = res_data.get("token") or res_data.get("data", {}).get("token")
                return self._token
        except Exception as e:
            logger.error(f"Error fetching Fabric Token: {str(e)}")
            return None

    def create_preorder(
        self,
        out_trade_no: Optional[str] = None,
        total_amount: Optional[float] = None,
        subject: Optional[str] = None,
    ) -> dict:
        trade_no = out_trade_no or self.out_trade_no or create_nonce_str(12)
        amount = total_amount or self.total_amount or 1.0
        title = subject or self.subject or "Bus Ticket"

        cleaned_trade_no = re.sub(r"[^A-Za-z0-9]", "", str(trade_no))
        if not cleaned_trade_no:
            cleaned_trade_no = f"ORDER{int(time.time())}"

        clean_merch_code = re.sub(r"[^A-Za-z0-9]", "", self.merchant_code)
        clean_merch_app_id = re.sub(r"[^0-9]", "", str(self.merchant_app_id)) or "1674185087411200"

        token = self._get_fabric_token()
        if not token:
            return {
                "success": False,
                "message": "Unable to acquire fabric auth token.",
            }

        try:
            formatted_amount = f"{float(amount):.2f}"
        except (ValueError, TypeError):
            formatted_amount = "1.00"

        notify_link = (
            self.notify_url
            if self.notify_url and "http" in self.notify_url
            else "https://www.google.com"
        )
        redirect_link = (
            self.redirect_url
            if self.redirect_url and "http" in self.redirect_url
            else "https://www.google.com"
        )

        # QR Code Scan ለማድረግ PayByQR ወይም Checkout የሚለውን trade_type መጠቀም ያስፈልጋል
        biz_content = {
            "appid": clean_merch_app_id,
            "business_type": "BuyGoods",
            "merch_code": clean_merch_code,
            "merch_order_id": str(cleaned_trade_no),
            "notify_url": notify_link,
            "payee_identifier": clean_merch_code,
            "payee_identifier_type": "04",
            "payee_type": "5000",
            "redirect_url": redirect_link,
            "short_code": clean_merch_code,
            "timeout_express": "120m",
            "title": str(title),
            "total_amount": str(formatted_amount),
            "trade_type": "Checkout",  # QR Scan እንዲሰራ ወደ PayByQR ተቀይሯል
            "trans_currency": "ETB",
        }

        req_payload = {
            "biz_content": biz_content,
            "method": "payment.preorder",
            "nonce_str": create_nonce_str(),
            "sign_type": "SHA256WithRSA",
            "timestamp": str(int(time.time())),
            "version": "1.0",
        }

        try:
            req_payload["sign"] = sign_payload_rsa_pss(
                req_payload, self.private_key_pem
            )
        except Exception as e:
            logger.error(f"Error signing Telebirr payload: {str(e)}")
            return {
                "success": False,
                "message": f"Failed to create RSA signature: {str(e)}",
            }

        headers = {
            "Content-Type": "application/json;charset=utf-8",
            "X-APP-Key": self.fabric_app_id,
            "Authorization": token,
        }

        url = f"{self.base_url}/payment/v1/merchant/preOrder"

        try:
            with httpx.Client(
                verify=False, follow_redirects=True, timeout=15.0
            ) as client:
                response = client.post(url, json=req_payload, headers=headers)
                res_data = response.json()

            code = str(res_data.get("code", ""))
            result = str(res_data.get("result", ""))

            if code == "0" or result == "SUCCESS":
                biz_res = res_data.get("biz_content", {})
                if isinstance(biz_res, str):
                    try:
                        biz_res = json.loads(biz_res)
                    except Exception:
                        biz_res = {}

                prepay_id = biz_res.get("prepay_id") or res_data.get("prepay_id")
                to_pay_url = biz_res.get("to_pay_url") or res_data.get("to_pay_url")
                to_pay_url_source = "api" if to_pay_url else None

                if not to_pay_url and prepay_id:
                    # preOrder for trade_type=Checkout returns only prepay_id; the
                    # checkout page URL must be built and signed separately per
                    # Ethio Telecom's "Generate Checkout Url" doc.
                    to_pay_url = self.build_checkout_url(prepay_id)
                    to_pay_url_source = "constructed"

                if to_pay_url:
                    receive_code = to_pay_url
                elif prepay_id:
                    receive_code = f"TELEBIRR$BUYGOODS${clean_merch_code}${formatted_amount}${prepay_id}$120m"
                else:
                    receive_code = None

                if not receive_code:
                    return {
                        "success": False,
                        "message": "Telebirr prepay_id or to_pay_url was not returned.",
                        "raw_response": res_data,
                    }

                return {
                    "success": True,
                    "prepay_id": prepay_id,
                    "to_pay_url": to_pay_url,
                    "to_pay_url_source": to_pay_url_source,
                    "receive_code": receive_code,
                    "raw_response": res_data,
                }
            else:
                logger.error(f"Telebirr PreOrder Error: {res_data}")
                return {
                    "success": False,
                    "message": res_data.get("msg")
                    or res_data.get("errorMsg", "Failed to initiate payment"),
                    "raw_response": res_data,
                }
        except Exception as e:
            logger.error(f"Telebirr PreOrder Exception: {str(e)}")
            return {"success": False, "message": str(e)}

    def create_order(
        self,
        out_trade_no: Optional[str] = None,
        total_amount: Optional[float] = None,
        subject: Optional[str] = None,
    ) -> dict:
        return self.create_preorder(out_trade_no, total_amount, subject)

    def build_checkout_url(self, prepay_id: str) -> str:
        clean_merch_code = re.sub(r"[^A-Za-z0-9]", "", self.merchant_code)
        clean_merch_app_id = re.sub(r"[^0-9]", "", str(self.merchant_app_id)) or self.merchant_app_id

        fields = {
            "appid": clean_merch_app_id,
            "merch_code": clean_merch_code,
            "nonce_str": create_nonce_str(),
            "prepay_id": str(prepay_id),
            "timestamp": str(int(time.time())),
        }
        fields["sign"] = sign_payload_rsa_pss(fields, self.private_key_pem)
        fields["sign_type"] = "SHA256WithRSA"

        raw_request = "&".join(
            f"{key}={urllib.parse.quote(str(fields[key]), safe='')}"
            for key in sorted(fields.keys())
        )
        return f"{self.web_base_url}?{raw_request}&version=1.0&trade_type=Checkout"

    def verify_callback_sign(self, payload: dict, signature: str) -> bool:
        return verify_sign_rsa(payload, self.public_key_pem, signature)

    def query_order(self, merch_order_id: str) -> dict:
        token = self._get_fabric_token()
        if not token:
            return {"success": False, "message": "Unable to acquire fabric auth token."}

        clean_merch_code = re.sub(r"[^A-Za-z0-9]", "", self.merchant_code)
        clean_merch_app_id = re.sub(r"[^0-9]", "", str(self.merchant_app_id)) or "1674185087411200"

        biz_content = {
            "appid": clean_merch_app_id,
            "merch_code": clean_merch_code,
            "merch_order_id": str(merch_order_id),
        }
        req_payload = {
            "biz_content": biz_content,
            "method": "payment.queryorder",
            "nonce_str": create_nonce_str(),
            "sign_type": "SHA256WithRSA",
            "timestamp": str(int(time.time())),
            "version": "1.0",
        }

        try:
            req_payload["sign"] = sign_payload_rsa_pss(
                req_payload, self.private_key_pem
            )
        except Exception as e:
            logger.error(f"Error signing Telebirr query payload: {str(e)}")
            return {"success": False, "message": str(e)}

        headers = {
            "Content-Type": "application/json;charset=utf-8",
            "X-APP-Key": self.fabric_app_id,
            "Authorization": token,
        }
        url = f"{self.base_url}/payment/v1/merchant/queryOrder"

        try:
            with httpx.Client(
                verify=False, follow_redirects=True, timeout=15.0
            ) as client:
                res = client.post(url, json=req_payload, headers=headers)
                return res.json()
        except Exception as e:
            logger.error(f"Query Order Error: {str(e)}")
            return {"success": False, "message": str(e)}


CreateOrderService = TelebirrService
