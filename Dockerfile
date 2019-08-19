FROM python:3.7
ADD . /code
WORKDIR /code

RUN curl -sL https://deb.nodesource.com/setup_10.x | bash - && \
    apt-get install -y nodejs
RUN curl -o- -L https://yarnpkg.com/install.sh | bash
RUN npm install -g serverless
RUN npm install

RUN pip install -r requirements.txt


