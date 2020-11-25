FROM python:3.8-alpine
RUN echo "https://mirrors.ustc.edu.cn/alpine/latest-stable/main" > /etc/apk/repositories \
    && apk update \
    && apk add --no-cache build-base npm nodejs \
    g++ bash make gcc\
    libffi-dev python3-dev \
    libffi git tzdata \
    freetype-dev lcms2-dev tiff-dev \
    linux-headers pcre-dev
RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone
RUN mkdir /vote
WORKDIR /vote
ADD ./requirements.txt /vote
RUN pip install -U pip -i https://pypi.douban.com/simple
RUN pip install -r requirements.txt -i https://pypi.douban.com/simple

ADD docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT [ "/docker-entrypoint.sh"]




