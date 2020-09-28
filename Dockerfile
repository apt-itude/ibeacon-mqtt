FROM balenalib/raspberrypi3-python:latest-build as build

WORKDIR /src/app

RUN install_packages libbluetooth-dev

ENV VIRTUALENV_DIR=/venv
ENV PATH="$VIRTUALENV_DIR/bin:$PATH"
RUN python -m venv $VIRTUALENV_DIR \
    && pip install -U "pip~=20.2" "setuptools~=50.3" "wheel~=0.35"

COPY setup.py .
COPY ibeacon_mqtt/ ibeacon_mqtt/

# beacontools has platform-specific deps, but no platform-specific wheels,
# so the wheel doesn't correctly depend on PyBluez, presumably because it wasn't
# built on Linux. This explicitly installs it from sdist to fix that.
RUN pip install --no-binary "beacontools" .

FROM balenalib/raspberrypi3-python:latest

RUN install_packages libbluetooth3

ENV VIRTUALENV_DIR=/venv
COPY --from=build $VIRTUALENV_DIR $VIRTUALENV_DIR

ENV PATH="$VIRTUALENV_DIR/bin:$PATH"

CMD ["ibeacon-mqtt"]
