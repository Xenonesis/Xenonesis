#!/usr/bin/env python3
"""
About Me Section Updater
Generates a dynamic "About Me" section for the README.md.
"""

import json
from typing import Dict, Any

class AboutMeUpdater:
    def __init__(self, analytics_data: Dict[str, Any]):
        self.data = analytics_data
        self.user_data = self.data.get("user_data", {})
        self.summary_metrics = self.data.get("summary_metrics", {})
        self.language_stats = self.data.get("language_stats", [])

    def generate_about_me_section(self) -> str:
        """Generates the new 'About Me' section in Markdown."""
        
        bio = self.user_data.get("bio", "A passionate developer and cybersecurity enthusiast.")
        name = self.user_data.get("name", "Aditya Kumar Tiwari")
        followers = self.user_data.get("followers", 0)
        following = self.user_data.get("following", 0)
        total_repos = self.summary_metrics.get("total_repositories", 0)
        total_stars = self.summary_metrics.get("total_stars", 0)

        top_languages = [lang["name"] for lang in self.language_stats[:5]]

        about_me_content = f"""
<div align="center">
  
  ## <img src="https://media.giphy.com/media/VgCDAzcKvsR6OM0uWg/giphy.gif" width="50"> About Me

  <p>
    <strong>{name}</strong>
  </p>
  <p>
    <em>{bio}</em>
  </p>

  <table>
    <tr>
      <td align="center">
        <strong>{followers}</strong>
        <br/>
        Followers
      </td>
      <td align="center">
        <strong>{following}</strong>
        <br/>
        Following
      </td>
      <td align="center">
        <strong>{total_repos}</strong>
        <br/>
        Repositories
      </td>
      <td align="center">
        <strong>{total_stars}</strong>
        <br/>
        Stars
      </td>
    </tr>
  </table>

  ### My Top Languages
  <p>
    {' | '.join(top_languages)}
  </p>
</div>
"""
        return about_me_content

    def update_readme(self, readme_path="README.md"):
        """Replaces the 'About Me' section in the README.md file."""
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()

        start_marker = '## <img src="https://media.giphy.com/media/VgCDAzcKvsR6OM0uWg/giphy.gif" width="50"> About Me'
        end_marker = '## <img src="https://media.giphy.com/media/WUlplcMpOCEmTGBtBW/giphy.gif" width="30"> Professional Experience'
        
        start_index = content.find(start_marker)
        end_index = content.find(end_marker)

        if start_index != -1 and end_index != -1:
            new_about_me = self.generate_about_me_section()
            new_content = content[:start_index] + new_about_me + "\n" + content[end_index:]
            
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print("Successfully updated the 'About Me' section in README.md")
        else:
            print("Could not find the 'About Me' section markers in README.md")

if __name__ == "__main__":
    try:
        with open("analytics-data.json", "r") as f:
            data = json.load(f)
        updater = AboutMeUpdater(data)
        updater.update_readme()
    except FileNotFoundError:
        print("analytics-data.json not found. Please run the main analytics script first.")
