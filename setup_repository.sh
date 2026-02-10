name: SWE-bench Pro Evaluation

on:
  workflow_dispatch:

jobs:
  evaluate:
    runs-on: ubuntu-latest
    container:
      image: manojva/openlibrary-python312:latest
      options: --user root

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup OpenLibrary repository
        run: bash setup_repository.sh

      - name: Pre-verification tests (EXPECTED TO FAIL)
        run: |
          cd /testbed
          python -m pytest openlibrary/tests/core/test_imports.py::TestImportItem::test_find_staged_or_pending -xvs \
          | tee /github/workspace/pre_verification.log
        continue-on-error: true

      - name: Run Claude Agent
        env:
          CLAUDE_API_KEY: ${{ secrets.CLAUDE_API_KEY }}
        run: python run_agent.py

      - name: Post-verification tests (MUST PASS)
        run: |
          cd /testbed
          python -m pytest openlibrary/tests/core/test_imports.py::TestImportItem::test_find_staged_or_pending -xvs \
          | tee /github/workspace/post_verification.log

      - name: Extract metrics
        run: python extract_metrics.py

      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: swebench-results
          path: |
            agent.log
            result.json
            pre_verification.log
            post_verification.log
            changes.patch
            prompts.md

