from flask import Flask, request, jsonify
from azure.storage.blob import BlobServiceClient, ContainerClient
import os

app = Flask(__name__)

# Replace these with your own Azure Blob Storage credentials
connection_string = "DefaultEndpointsProtocol=https;AccountName=azuretestshubham832458;AccountKey=2yEaP59qlgKVv6kEUCA5ARB4wdV3ZRoL2X9zjYCcIxOSYAG1CSBbBlAMPx3uBIe7ilQtSh7purEK+AStvFn8GA==;EndpointSuffix=core.windows.net"

# Initialize the BlobServiceClient using your connection string
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Function to create the "transcript" folder if it doesn't exist
def create_transcript_folder():
    folder_path = "transcript"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# Route to download a blob
@app.route('/download', methods=['POST'])
def download_blob():
    try:
        data = request.get_json()
        container_name = data.get('container_name')
        blob_name = data.get('blob_name')
        local_file_path = f"transcript/{blob_name}"  # Change this path as needed

        # Create the "transcript" folder if it doesn't exist
        create_transcript_folder()

        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)

        with open(local_file_path, "wb") as local_file:
            blob_data = blob_client.download_blob()
            blob_data.readinto(local_file)

        return jsonify({"message": f"Blob {blob_name} has been downloaded to {local_file_path}"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to delete all blobs in a container
@app.route('/delete', methods=['POST'])
def delete_all_blobs_in_container():
    try:
        data = request.get_json()
        container_name = data.get('container_name')

        container_client = blob_service_client.get_container_client(container_name)
        blobs = container_client.list_blobs()

        for blob in blobs:
            container_client.delete_blob(blob.name)

        return jsonify({"message": f"All blobs in container {container_name} have been deleted."})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
