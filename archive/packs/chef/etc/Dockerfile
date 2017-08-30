# Testing node for Chef
FROM dockerfile/ubuntu

# Disable prompts
ENV DEBIAN_FRONTEND noninteractive

# Install ssh
RUN apt-get update && apt-get install -y ssh && mkdir /var/run/sshd

# Create stanley
RUN useradd -m -s /bin/bash stanley ; \
    sudo -u stanley mkdir /home/stanley/.ssh ; \
    chmod 750 /home/stanley/.ssh ; \
    echo "stanley ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/st2 ; \
    chmod 440 /etc/sudoers.d/st2 ; \
    echo stanley:stanley | chpasswd

EXPOSE 22

CMD /usr/sbin/sshd -D
