# Project File Structure
```
./
    .env
    .gitignore
    agent1.ipynb
    agent1_1.ipynb
    generate_README.py
    ipynb_to_py.py
    README.md
    requirements.txt
    run.py
    .ipynb_checkpoints/
        agent1-checkpoint.ipynb
        agent1.1-checkpoint.ipynb
        agent1_1-checkpoint.ipynb
    app/
        config.py
        routes.py
        __init__.py
        test/
            mysql.py
            TestRoute.py
        views/
            AgentRoute.py
            __init__.py
            Agent/
                agent.py
                CenterAgent1_1_cmd.py
                CenterAgent1_1_input.py
                CenterAgent1_1_main.py
                CenterAgent_main.py
                __init__.py
    config/
        mysql_config.py
    generated_plans/
        111_plan.md
    models/
        _init_.py
    services/
        langserve_service.py
    tests/
        test_agent
        test_routes.py
    utils/
        generate_md.py
        ProjectTree.py
        README.md
        stage1_md_to_mysql.py
```
