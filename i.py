import streamlit as st
import requests
import json
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
# Set the AbuseIPDB API key
API_KEY = "a9b4d5a56c7f0898630d7868efcfa19eef37a07f1b7a76789938eee78122119fdb562e26f5567e06"

# Set the base URL for the AbuseIPDB API
BASE_URL = "https://api.abuseipdb.com/api/v2/check"

# Streamlit App
def main():
    # Title and instructions
    st.title("AbuseIPDB Checker")
    st.markdown(
        """
        Enter an IP address to check its abuse reports using the AbuseIPDB API.
        """
    )

    # Input for the IP address
    ip_address = st.text_input("Enter the IP address:")

    # Optional: Input for maxAgeInDays
    max_age = st.slider("Max Age of Reports (days):", min_value=1, max_value=365, value=30)

    # Submit button
    if st.button("Check IP"):
        if ip_address:
            result = check_ip(ip_address, max_age)
            if result:
                display_result(result)
            else:
                st.error("Unable to retrieve data. Check the IP address or try again later.")
        else:
            st.warning("Please enter a valid IP address.")

# Function to query the AbuseIPDB API
def check_ip(ip_address, max_age):
    headers = {
        "Accept": "application/json",
        "Key": API_KEY
    }
    params = {
        "ipAddress": ip_address,
        "maxAgeInDays": max_age
    }

    try:
        response = requests.get(BASE_URL, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
        return None

# Function to display the result
def display_result(data):
    st.subheader("AbuseIPDB Report")
    ip_data = data.get("data", {})

    if ip_data:
        st.write(f"**IP Address:** {ip_data.get('ipAddress')}")
        st.write(f"**Abuse Confidence Score:** {ip_data.get('abuseConfidenceScore')}%")
        st.write(f"**Country:** {ip_data.get('countryName', 'Unknown')}")
        st.write(f"**ISP:** {ip_data.get('isp', 'Unknown')}")
        st.write(f"**Domain:** {ip_data.get('domain', 'Unknown')}")
        st.write(f"**Number of Reports:** {ip_data.get('totalReports', 0)}")
        st.write(f"**Last Reported At:** {ip_data.get('lastReportedAt', 'Never')}")

        # Show reports if available
        reports = ip_data.get("reports", [])
        if reports:
            st.subheader("Reports")
            for report in reports:
                st.markdown(f"- **Reported At:** {report.get('reportedAt', 'Unknown')}")
                st.markdown(f"  **Categories:** {', '.join(map(str, report.get('categories', [])))}")
                st.markdown(f"  **Comment:** {report.get('comment', 'No comment provided.')}")
        else:
            st.info("No reports available for this IP.")
    else:
        st.warning("No data available for the IP address.")

if __name__ == "__main__":
    main()
