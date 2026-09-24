# Demo

Run the classification demo:

```bash
python3 run_demo.py sample_inbox.json
```

Run the regression tests from repository root:

```bash
python3 tests/test_demo.py
```

Rebuild the narrated MP4 in a virtual environment:

```bash
python3 -m venv .demo-venv
.demo-venv/bin/pip install -r demo/requirements.txt
.demo-venv/bin/python demo/build_video.py
```

The fixtures are sanitized and synthetic. The offline demo never connects to a mailbox, sends email, spends funds, or signs a wallet. Its purpose is to demonstrate the work-packet classification and safety rules deterministically before substituting real bounded Mermail MCP reads.
