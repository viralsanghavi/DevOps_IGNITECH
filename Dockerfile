FROM centos:7

RUN yum update -y \
    && yum install -y https://centos7.iuscommunity.org/ius-release.rpm \
    && yum install -y python36u python36u-libs python36u-devel python36u-pip \
    && yum install -y which gcc \ 
    && yum install -y openldap-devel \
   && yum install -y  mariadb-devel
# pipenv installation
RUN pip3.6 install pipenv

RUN ln -s /usr/bin/pip3.6 /bin/pip

RUN rm /usr/bin/python

# python must be pointing to python3.6
RUN ln -s /usr/bin/python3.6 /usr/bin/python

#RUN python --version

RUN mkdir -p /DEVOPS-IGNITECH 

COPY . /DEVOPS-IGNITECH/

WORKDIR /DEVOPS-IGNITECH/ 

RUN pip install --upgrade pip && \
    pip install --no-cache-dir mysql && \
    pip install --no-cache-dir flask_mysqldb


EXPOSE 5000

CMD ["python","app.py"] 
