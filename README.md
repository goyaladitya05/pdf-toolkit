# PDF Toolkit

## Why I built this

I don't trust handing my PDFs to online tools. 

So this does it **entirely on your own machine**. Nothing is uploaded anywhere.

## What it does

- **Encrypt** a PDF with a password.
- **Decrypt** a PDF you have the password for.

More PDF operations (merge, split, compress…) may come later.

## How to use

```bash
pip install -r requirements.txt
cd backend
python run.py
```

Open <http://127.0.0.1:8000>, drop in a PDF, enter a password, and download the
result.

## License

MIT — see [LICENSE](LICENSE).
