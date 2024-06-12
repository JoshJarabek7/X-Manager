# X-Manager

Manage your account on X without having to create a developer account and use their API.

It's done entirely using Selenium and Python to login and load/search/delete your tweets/likes/replies/retweets.

Done entirely local and free!

Requires you to request your profile/data archive from X and then send it to the backend. The data will be parsed and updated to the MongoDB Database in the Docker Compose file. The backend and selenium will then use that database, as well as websockets to the frontend, to update your profile, database, and frontend in real-time.

Uses breaks and randomization to adhere to X's rate limits for tweet/likes/etc deletion.

Still a Work-in-Progress.

Plans for:

- SvelteKit frontend to:
    - Select tweets/likes/etc you want deleted
    - See who your fans are (followers you're not following)
    - See who you're a fan of (following accounts that aren't following you)
    - Input your SMS 2FA or Email 2FA if X asks for it

- Integration of any other ideas as we go along