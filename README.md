# Carbon Black & Binalyze AIR Integration Script

This script integrates Carbon Black Cloud (CBC) and Binalyze AIR. It is written in Python and uses the CBAPI library to interact with the CB Defense platform. The script listens for notifications from CB, and when a new alert is detected, it sends an acquisition request to the Binalyze AIR instance specified in the `air_webhook` variable.

## Prerequisites

- Carbon Black Defense API key with access level type.
- Binalyze AIR instance URL and a configured webhook.
- Creating a credentials.psc file with the help of `cbapi-defense configure`
- Docker.
- Correctly configured `.env` file.
- A machine that has Network Connection to both Binalyze Air and Carbon Black instances.

## Configuration

### Navigate to Carbon Black Cloud Console
1. Create API Key
   1. Navigate to **Settings** > **API Keys** > **Add API Key**
   2. Create API Key with *Access Level* **SIEM** and Copy both keys:
      1. **API ID** *Connector ID*.
      2. **API Secret Key** *API Key*.
2. Create an Alert Notification
   1. Navigate to **Settings** > **Notification** > **Add Notification**.
      1. Fill in all the necessary details.
      2. Select the **Created API Key** on the first step.
      3. Save.

### Navigate to Binalyze AIR Console
3. Create a webhook.
   1. Click the webhook on the left-hand pane.
   2. Click **+ New Webhook**.
   3. Select **Carbon Black Parser** from **Parser**.
   4. Fill in all the necessary information and save.
   5. Copy the **webhook URL**, and paste it to the value of `AIR_WEBHOOK_URL` in `.env:1`.

### Navigate the environment you want to run the script.
4. Create `credentials.defense` file [click here](https://cbapi.readthedocs.io/en/latest/#api-credentials) for more information.
   1. First, [install cbapi](https://cbapi.readthedocs.io/en/latest/installation.html#installation) 
   2. Run `cbapi-defense configure` and follow the instructions. Please refer [Carbon Black Documentation](https://developer.carbonblack.com/reference/enterprise-response/guide/getting-started-with-the-cbapi/) for more information.
   3. A `credentials.defense` file will be created, and copy its contents to the file in this directory(or replace).
   4. Copy the Carbon Black instance [hostname](https://developer.carbonblack.com/reference/carbon-black-cloud/authentication#construct-your-request) and paste it to the value of CB_DEFENSE_SERVER in `.env:2`

## Usage

1. Clone the repo.
2. Follow the **Configuration** part and make the proper changes.
3. Run ``docker build -t carbonblack-air-integration .`` and finally `docker run --env-file=.env carbonblack-air-integration`
4. The script will start running and will listen for new alerts from CarbonBlack. Once a new alert is detected, it will send an acquisition request to the specified Binalyze AIR instance.
5. A message appears when an acquisition request has been sent to the device.
6. The script will print the error message and log it in the `integration.log` file if an error occurs.

## Note

- The script uses the `time` and `requests` libraries. 
- The script can be stopped by pressing `Ctrl + C`.
- The script  queries the alerts from Carbon Black, writes to `query.json`  and sends a request to Binalyze AIR Console.
- The script logs all the errors it encounters in `integration.log` file.
