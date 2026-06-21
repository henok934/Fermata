for file in *.html; do
    # Check if the "Register Driver" line exists
    if grep -q '<li class="main_nav_item"><a href="{% url '\''worker'\'' %}">Register Driver</a></li>' "$file"; then
        # Check if the "BusInsert" line already exists
        if ! grep -q '<li class="main_nav_item"><a href="{% url '\''businsert'\'' %}">BusInsert</a></li>' "$file"; then
            # Add the "BusInsert" line at the end of the file
            echo '<li class="main_nav_item"><a href="{% url '\''businsert'\'' %}">BusInsert</a></li>' >> "$file"
        fi
    fi
done
