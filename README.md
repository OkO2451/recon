# recon

/my_automation_project
    /src
        /my_automation_project
            __init__.py
            module1.py
            module2.py
    /tests
        test_module1.py
        test_module2.py
    /scripts
        run_tool1.py
        run_tool2.py
    /docs
        index.md
    /examples
        example1.py
        example2.py
    /data
        sample_data.csv
    /notebooks
        exploration.ipynb
    /config
        settings.ini
    README.md
    LICENSE
    setup.py
    requirements.txt
    .gitignore

## Docker

### usage

#### building

```bash
docker build -t dns_recon_tool .

```

#### runinig the machine

- passive

```bash
docker run --rm dns_recon --mode passive example.com

```

- active

```bash
docker run --rm dns_recon --mode active example.com

```
