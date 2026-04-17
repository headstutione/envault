# envault

> CLI tool to manage and encrypt project environment variables with team-sharing support

---

## Installation

```bash
pip install envault
```

Or with pipx for isolated installs:

```bash
pipx install envault
```

---

## Usage

Initialize envault in your project:

```bash
envault init
```

Add and encrypt an environment variable:

```bash
envault set DATABASE_URL "postgres://user:pass@localhost/db"
```

Share encrypted variables with your team:

```bash
envault export --output .envault.enc
envault import .envault.enc
```

Load variables into your current shell session:

```bash
eval $(envault load)
```

View all stored keys (without exposing values):

```bash
envault list
```

---

## How It Works

envault encrypts your environment variables using AES-256 and stores them in a versioned `.envault` file that can be safely committed to source control. Team members decrypt variables using a shared key or public/private key pairs.

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## License

This project is licensed under the [MIT License](LICENSE).