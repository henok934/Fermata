
import re



with open("sc.html", "r") as f:

    content = f.read()



# Define the exact new navigation dropdowns block

new_block = """<select onchange="if(this.value != '#') location.href = this.value;" class="custom-nav-select mx-xl-1">

    <option value="#" selected disabled>Registry</option>



    <option value="{% url 'route' %}" {% if not user.is_approved %}disabled style="color: #999;"{% endif %}>

        Define New Route {% if not user.is_approved %}(Disabled){% endif %}

    </option>



    {% if user.city == "Addis Ababa" %}

        <option value="{% url 'sc' %}" {% if not user.is_approved %}disabled style="color: #999;"{% endif %}>

            Register Share Company {% if not user.is_approved %}(Disabled){% endif %}

        </option>

        <option value="{% url 'registor' %}" {% if not user.is_approved %}disabled style="color: #999;"{% endif %}>

            Add System Admin {% if not user.is_approved %}(Disabled){% endif %}

        </option>

        <option value="{% url 'worker' %}" {% if not user.is_approved %}disabled style="color: #999;"{% endif %}>

            Register Ticket Agent {% if not user.is_approved %}(Disabled){% endif %}

        </option>

        <option value="{% url 'city' %}" {% if not user.is_approved %}disabled style="color: #999;"{% endif %}>

            Add Terminal Hub {% if not user.is_approved %}(Disabled){% endif %}

        </option>

        <option value="{% url 'service_fee' %}" {% if not user.is_approved %}disabled style="color: #999;"{% endif %}>

            Set Service Tariff {% if not user.is_approved %}(Disabled){% endif %}

        </option>

    {% endif %}

</select>

<select onchange="if(this.value != '#') location.href = this.value;" class="custom-nav-select mx-xl-1">

    <option value="#" selected disabled>System Configuration</option>

    <option value="{% url 'active' %}" {% if not user.is_approved %}disabled style="color: #999;"{% endif %}>

        Active Deployments {% if not user.is_approved %}(Disabled){% endif %}

    </option>

    <option value="{% url 'act' %}" {% if not user.is_approved %}disabled style="color: #999;"{% endif %}>

        Change Bus {% if not user.is_approved %}(Disabled){% endif %}

    </option>



    {% if user.city == "Addis Ababa" %}

        <option value="{% url 'scupdate' %}" {% if not user.is_approved %}disabled style="color: #999;"{% endif %}>

            Edit Share Company {% if not user.is_approved %}(Disabled){% endif %}

        </option>

        <option value="{% url 'serviceupdate' %}" {% if not user.is_approved %}disabled style="color: #999;"{% endif %}>

            Tariff Adjustment {% if not user.is_approved %}(Disabled){% endif %}

        </option>

    {% endif %}

</select>

<select onchange="if(this.value != '#') location.href = this.value;" class="custom-nav-select mx-xl-1">

    <option value="#" selected disabled>System Analytics</option>

    <option value="{% url 'routes' %}" {% if not user.is_approved %}disabled style="color: #999;"{% endif %}>

        Route Mapping {% if not user.is_approved %}(Disabled){% endif %}

    </option>

    <option value="{% url 'ticketinfo' %}" {% if not user.is_approved %}disabled style="color: #999;"{% endif %}>

        Booked Tickets {% if not user.is_approved %}(Disabled){% endif %}

    </option>

    <option value="{% url 'totalballance' %}" {% if not user.is_approved %}disabled style="color: #999;"{% endif %}>

        Revenue Analytics {% if not user.is_approved %}(Disabled){% endif %}

    </option>

    <option value="{% url 'sce' %}" {% if not user.is_approved %}disabled style="color: #999;"{% endif %}>

        View Share Companies {% if not user.is_approved %}(Disabled){% endif %}

    </option>



    {% if user.city == "Addis Ababa" %}

        <option value="{% url 'users' %}" {% if not user.is_approved %}disabled style="color: #999;"{% endif %}>

            User Registry {% if not user.is_approved %}(Disabled){% endif %}

        </option>

        <option value="{% url 'buses' %}" {% if not user.is_approved %}disabled style="color: #999;"{% endif %}>

            View Buses {% if not user.is_approved %}(Disabled){% endif %}

        </option>

        <option value="{% url 'comments' %}" {% if not user.is_approved %}disabled style="color: #999;"{% endif %}>

            Passenger Feedback {% if not user.is_approved %}(Disabled){% endif %}

        </option>

    {% endif %}



    <option value="{% url 'driver' %}" {% if not user.is_approved %}disabled style="color: #999;"{% endif %}>

        Booker Registry {% if not user.is_approved %}(Disabled){% endif %}

    </option>

</select>"""



# Target the first signature legacy green select up to the 4th legacy block closure

pattern = r'<select onchange="location\.href = this\.value;" class="custom-select".*?<\/select>\s*<\/li>\s*<\/li>\s*<\/li>\s*<\/li>'



# Replace the old blocks smoothly regardless of weird white spaces

modified, count = re.subn(r'(<select onchange="location\.href = this\.value;".*?<\/select>\s*<\/li>\s*){4}', new_block + "\n", content, flags=re.DOTALL)



if count > 0:

    with open("sc.html", "w") as f:

        f.write(modified)

    print("Success: Updated old select menus with new customized nav block!")

else:

    # Backup flexible split method if regex variant signature layout changes

    parts = content.split('<select onchange="location.href = this.value;" class="custom-select"')

    if len(parts) >= 5:

        # Rebuild file bypassing the 4 old select segments

        remainder = parts[4].split('</select>', 1)[1]

        new_content = parts[0] + new_block + remainder

        with open("sc.html", "w") as f:

            f.write(new_content)

        print("Success: Updated via layout segment split mapping!")

    else:

        print("Error: Could not locate the 4 legacy select items context inside sce.html.")

