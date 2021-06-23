.PHONY: clean
clean:
    rm -rf cdk.out
    rm -f cdk.staging
    find . -name '.tox' -exec rm -fr {} +
    find . -name '.coverage' -exec rm -fr {} +
    find . -name '*.egg-info' -exec rm -fr {} +
    find . -name '__pycache__' -exec rm -fr {} +
    find . -name '.pytest_cache' -exec rm -fr {} +

.PHONY: synth
synth:
    cdk synth
