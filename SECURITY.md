# Security Guidelines for Crunevo

This document summarizes how passwords and administrative users are managed.

## Password Handling
- All passwords are hashed using Werkzeug's `generate_password_hash` with the `scrypt` method.
- Plain text passwords are never stored in the database.
- The `User.set_password` method automatically hashes the provided password.
- Passing a pre-generated hash to `set_password` raises an error to avoid invalid records.

## Creating Admin Users
- Use `scripts/create_user.py` to create any new account from the command line:
  ```bash
  python scripts/create_user.py EMAIL USERNAME PASSWORD --role admin
  ```
- The script inserts the user with the specified role and hashes the password using `scrypt`.
- Avoid inserting rows manually in the database to prevent malformed hashes.

## Emergency Access
- A master password can be configured via the environment variable `MASTER_KEY`.
- Set `ENABLE_MASTER_KEY=0` to disable this feature entirely.
- When a login attempt provides the master password, the system logs a
  `[MASTER LOGIN]` message and grants access to the specified account without the
  regular password check.
- Use this only for critical situations and rotate the key periodically.

## Logging
- The application configures a rotating file log under `instance/crunevo.log`.
- Sensitive data such as passwords is never logged.

## Common Pitfalls
- Do **not** store or expose plain text passwords.
- Ensure `SQLALCHEMY_DATABASE_URI` and `SECRET_KEY` are set correctly in `.env`.
- If a user record contains an invalid password hash, recreate the user using the script above.
