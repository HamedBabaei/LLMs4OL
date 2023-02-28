FROM jupyter/minimal-notebook:latest

ARG conda_env=python3
ARG py_ver=3.9

RUN conda create --quiet --yes -p $CONDA_DIR/envs/$conda_env python=$py_ver ipython jupyterlab ipykernel htop && \
    conda clean --all -f -y

RUN $CONDA_DIR/envs/${conda_env}/bin/python -m ipykernel install --user --name=${conda_env} && \
    fix-permissions $CONDA_DIR && fix-permissions /home/$NB_USER

RUN $CONDA_DIR/envs/${conda_env}/bin/pip install torch torchvision torchaudio

ENV PATH $CONDA_DIR/envs/${conda_env}/bin:$PATH

ENV CONDA_DEFAULT_ENV ${conda_env}
