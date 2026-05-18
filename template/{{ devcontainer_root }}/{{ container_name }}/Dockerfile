FROM debian:12

ARG TZ
ENV TZ="$TZ"

ARG CLAUDE_CODE_VERSION=stable
ARG GIT_DELTA_VERSION=0.18.2
ARG USERNAME=claude

# Install basic development tools and iptables/ipset
RUN apt-get update && apt-get install -y --no-install-recommends \
  ca-certificates \
  less \
  git \
  procps \
  sudo \
  fzf \
  zsh \
  man-db \
  unzip \
  gnupg2 \
  gh \
  iptables \
  ipset \
  iproute2 \
  dnsutils \
  aggregate \
  jq \
  nano \
  vim \
  curl \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create claude user
RUN useradd -m -s /bin/zsh $USERNAME

# Persist bash history
RUN mkdir /commandhistory \
  && touch /commandhistory/.bash_history \
  && chown -R $USERNAME /commandhistory

# Set `DEVCONTAINER` environment variable to help with orientation
ENV DEVCONTAINER=true

# Create workspace and config directories and set permissions
RUN mkdir -p /workspace /home/$USERNAME/.claude && \
  chown -R $USERNAME:$USERNAME /workspace /home/$USERNAME/.claude

WORKDIR /workspace

# Install git-delta
RUN ARCH=$(dpkg --print-architecture) && \
  curl -fsSL "https://github.com/dandavison/delta/releases/download/${GIT_DELTA_VERSION}/git-delta_${GIT_DELTA_VERSION}_${ARCH}.deb" \
    -o /tmp/git-delta.deb && \
  dpkg -i /tmp/git-delta.deb && \
  rm /tmp/git-delta.deb

COPY --chown=$USERNAME:$USERNAME zshrc /home/$USERNAME/.zshrc
COPY --chown=$USERNAME:$USERNAME p10k.zsh /home/$USERNAME/.p10k.zsh
COPY --chown=$USERNAME:$USERNAME gitconfig /home/$USERNAME/.gitconfig

USER $USERNAME

# Install Claude Code
RUN curl -fsSL https://claude.ai/install.sh | bash -s -- "${CLAUDE_CODE_VERSION}"


ENV SHELL=/bin/zsh

# Install powerlevel10k theme
RUN git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ~/powerlevel10k

# Copy and set up firewall and startup scripts
COPY init-firewall.sh startup.sh /usr/local/bin/
USER root
RUN chmod +x /usr/local/bin/init-firewall.sh /usr/local/bin/startup.sh && \
  echo "$USERNAME ALL=(root) NOPASSWD:SETENV: /usr/local/bin/init-firewall.sh" > /etc/sudoers.d/$USERNAME-firewall && \
  chmod 0440 /etc/sudoers.d/$USERNAME-firewall

USER $USERNAME
