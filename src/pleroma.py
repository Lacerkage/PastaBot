import requests


class Pleroma():
    def __init__(self, instance_url, access_token):
        self.instance_url = instance_url
        self.api_url = f"{instance_url}/api/v1"
        self.access_token = access_token

    def delete_status(self, id):
        res = requests.delete(f"{self.api_url}/statuses/{id}", headers={
            "Authorization": f"Bearer {self.access_token}"
        })

        if not res.ok:
            res.raise_for_status()

        print(f"Deleted status {id}")

    def purge(self):
        account_id = "ANsxILwMPM70O4URma"  # TODO: Dynamically set it
        res = requests.get(f"{self.api_url}/accounts/{account_id}/statuses")

        if not res.ok:
            res.raise_for_status()

        for status in res.json():
            self.delete_status(status["id"])

    def upload_media(self, media):
        res = requests.post(
            f"{self.api_url}/media",
            files={
                "file": media
            },
            headers={
                "Authorization": f"Bearer {self.access_token}"
            }
        )

        if not res.ok:
            res.raise_for_status()

        return res.json()

    def post_status(self, body, sensitive=False, media=[]):
        media_ids = []

        if len(media) != 0:
            for file in media:
                attachment = self.upload_media(file)

                media_ids.append(attachment["id"])

        res = requests.post(
            f"{self.api_url}/statuses",
            json={
                "sensitive": sensitive,
                "status": body,
                "content_type": "text/markdown",
                "media_ids": media_ids,
                "visibility": "private"
            },
            headers={
                "Authorization": f"Bearer {self.access_token}"
            }
        )

        if not res.ok:
            res.raise_for_status()

        return True
