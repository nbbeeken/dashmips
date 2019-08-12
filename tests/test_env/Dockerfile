FROM python:3.7.3-stretch as builder

ARG ENV

RUN useradd -ms /bin/bash mips
USER mips
RUN chown mips:mips -R /home/mips

RUN mkdir -p /home/mips/dashmips /home/mips/.config/pip/
RUN printf "[global]\nuser=true\n" > /home/mips/.config/pip/pip.conf && cat /home/mips/.config/pip/pip.conf

WORKDIR /home/mips/dashmips

ENV ENV=${ENV} \
    HOME=/home/mips \
    PATH=/home/mips/.local/bin:$PATH \
    PYTHONPATH=/home/mips/dashmips/src:${PYTHONPATH} \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.0.0a5 \
    POETRY_PREVIEW=1


# System deps:
RUN pip install --user -U pip setuptools
RUN pip install --user "poetry==$POETRY_VERSION"


# Copy all
COPY . .

# Project initialization:
RUN mkdir -p /home/mips/.config/pypoetry/ && touch /home/mips/.config/pypoetry/config.toml
RUN poetry config settings.virtualenvs.create false
RUN poetry export -f requirements.txt

FROM python:3.7.3-alpine
RUN mkdir -p /app/dashmips /app/mips
WORKDIR /app

ENV PYTHONPATH /home/mips/dashmips/src:${PYTHONPATH}
ENV PIP_DISABLE_PIP_VERSION_CHECK on

COPY --from=builder /home/mips/dashmips/src/dashmips dashmips
COPY --from=builder /home/mips/dashmips/requirements.txt .
COPY --from=builder /home/mips/dashmips/tests/test_mips mips

RUN pip install --user -r requirements.txt
CMD python -m dashmips run /app/mips/strings.mips
