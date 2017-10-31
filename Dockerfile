FROM ubuntu:16.04

#ARG GEOS_VERSION=3.4.2
#ARG PROJ4_VERSION=4.9.1
#ARG PROJ4_DATUMGRID_VERSION=1.5
ARG GDAL_VERSION=2.1.0
ARG ENTRYKIT_VERSION=0.4.0

ENV PRJ_ROOT /opt/hacku
ENV TZ Asia/Tokyo

RUN mkdir /workdir && \
    mkdir /opt/iot_stick

WORKDIR workdir

RUN apt-get update -y && \
    apt-get install -y \
        python3 \
        python3-pip && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone

# Not required ?
#RUN apt-get update -y && \
#    apt-get install -y \
#        binutils \
#        libproj-dev \
#        gdal-bin \
#        wget \
#        make \
#        g++ \
#        bzip2 && \
#    wget http://download.osgeo.org/geos/geos-${GEOS_VERSION}.tar.bz2 && \
#    tar xjf geos-${GEOS_VERSION}.tar.bz2 && \
#    cd geos-${GEOS_VERSION} && \
#    ./configure && make && make install && cd ../ && \
#    wget http://download.osgeo.org/proj/proj-${PROJ4_VERSION}.tar.gz && \
#    wget http://download.osgeo.org/proj/proj-datumgrid-${PROJ4_DATUMGRID_VERSION}.tar.gz && \
#    tar xzf proj-${PROJ4_VERSION}.tar.gz && \
#    cd proj-${PROJ4_VERSION}/nad && \
#    tar xzf ../../proj-datumgrid-${PROJ4_DATUMGRID_VERSION}.tar.gz && cd ../ && \
#    ./configure && make && make install && cd ../ && \
#    wget http://download.osgeo.org/gdal/${GDAL_VERSION}/gdal-${GDAL_VERSION}.tar.gz && \
#    tar xzf gdal-${GDAL_VERSION}.tar.gz && \
#    cd gdal-${GDAL_VERSION} && ./configure && make && make install && cd ../ && \
#    apt-get remove --purge -y \
#        wget \
#        g++ \
#        bzip2 \
#        make && \
#    apt-get autoremove -y && \
#    apt-get -y autoclean && \
#    rm geos-${GEOS_VERSION}.tar.bz2 && \
#    rm proj-${PROJ4_VERSION}.tar.gz && \
#    rm proj-datumgrid-${PROJ4_DATUMGRID_VERSION}.tar.gz && \
#    rm gdal-${GDAL_VERSION}.tar.gz && \
#    rm -r geos-${GEOS_VERSION} && \
#    rm -r proj-${PROJ4_VERSION} && \
#    rm -r proj-datumgrid-${PROJ4_DATUMGRID_VERSION} && \
#    rm -r gdal-${GDAL_VERSION}
RUN apt-get update -y && \
    apt-get install -y \
        binutils \
        libproj-dev \
        gdal-bin \
        wget \
        make \
        g++ \
        bzip2 && \
    wget http://download.osgeo.org/gdal/${GDAL_VERSION}/gdal-${GDAL_VERSION}.tar.gz && \
    tar xzf gdal-${GDAL_VERSION}.tar.gz && \
    cd gdal-${GDAL_VERSION} && ./configure && make && make install && cd ../ && \
    apt-get remove --purge -y \
        wget \
        g++ \
        bzip2 \
        make && \
    apt-get autoremove -y && \
    apt-get -y autoclean && \
    rm gdal-${GDAL_VERSION}.tar.gz && \
    rm -r gdal-${GDAL_VERSION}

# Install Entrykit
#RUN apt-get update -y && \
#    apt-get install -y \
#        curl && \
#    curl -LO https://github.com/progrium/entrykit/releases/download/v${ENTRYKIT_VERSION}/entrykit_${ENTRYKIT_VERSION}_Linux_x86_64.tgz && \
#    tar zxf entrykit_${ENTRYKIT_VERSION}_Linux_x86_64.tgz && \
#    mv entrykit /bin/entrykit && \
#    chmod +x /bin/entrykit && \
#    entrykit --symlink && \
#    rm entrykit_${ENTRYKIT_VERSION}_Linux_x86_64.tgz && \
#    apt-get remove --purge -y \
#        curl && \
#    apt-get -y autoremove && \
#    apt-get -y autoclean

COPY ./src/iot_stick ${PRJ_ROOT}

WORKDIR ${PRJ_ROOT}

# Install Python libraries
RUN apt-get update -y && \
    apt-get install -y \
        g++ && \
    pip3 --no-cache-dir install -r requirements.txt && \
    apt-get remove --purge -y g++ && \
    apt-get autoremove -y && \
    apt-get autoclean -y

#ENV GEOS_LIBRARY_PATH '/usr/local/lib/libgeos_c.so'
ENV GDAL_LIBRARY_PATH '/usr/local/lib/libgdal.so'
ENV LD_LIBRARY_PATH '/usr/local/lib'
