# api_clients/github_api.py
from api_clients.base_client import BaseAPIClient
from models.repo_model import RepositoryModel
from config.env_data import GITHUB_USERNAME

class GithubAPI(BaseAPIClient):

    def create_private_repo(self, repo_name: str) -> RepositoryModel:
        endpoint = '/user/repos'
        payload = {'name': repo_name, 'private': True, 'auto_init': True}

        print(f"API Setup: Creating private repository '{repo_name}'...")

        # Because of _handle_response, 'response_data' is already a parsed dictionary!
        # If the call failed, _handle_response would have already raised an Exception.
        res_data = self.post(endpoint, payload)

        # Pass the dictionary directly into your strict Pydantic model
        valid_repo_data = RepositoryModel(**res_data)
        
        return valid_repo_data

    def delete_repo(self, repo_name: str):
        endpoint = f'/repos/{GITHUB_USERNAME}/{repo_name}'

        print(f"API Setup: Deleting repository '{repo_name}'...")

        # Because of _handle_response, this will return True if it succeeds (204 No Content)
        return self.delete(endpoint)