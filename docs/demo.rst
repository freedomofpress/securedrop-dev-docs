demo.securedrop.org
===================

There is a deployment of SecureDrop server running at https://demo.securedrop.org/ that is very similar
to ``make dev``. Changes pushed to the ``develop`` branch automatically get deployed there.

How it works
------------
Deployment is managed in Codefresh, which we use for other Kubernetes-related CI/CD; if you want to look at
build logs or (re)start pipelines and don't have access, ask someone from the infra team. This is not a
requirement to be able to update and deploy the demo; you just need to be able to push to the SecureDrop
repo's ``develop`` branch.

Containers
----------
There are two containers in the `securedrop <https://github.com/freedomofpress/securedrop>`_ repo:

* ``securedrop/dockerfiles/focal/python3/DemoDockerfile``
* ``devops/demo/landing-page/Dockerfile``

If you want to try these locally, build them from the root of the SecureDrop repository, using
``docker build -f FILE .``. The "landing page" container is what you see at https://demo.securedrop.org/
and the main container serves both https://demo-source.securedrop.org/ and
https://demo-journalist.securedrop.org/

Troubleshooting
---------------
The deployment is not highly available, and everything in Redis is thrown away when it restarts. When
restarting, the source and journalist interfaces will both be unavailable for a few seconds and you'll
see a 503.

If you need to cause a restart without pushing a new deployment, or roll back to an earlier version, ask
the infra team. These can be done quickly but require direct Kubernetes access.
