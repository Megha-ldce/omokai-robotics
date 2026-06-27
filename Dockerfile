FROM ros:jazzy-ros-base

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3.12-venv \
    ros-jazzy-turtlebot3 \
    ros-jazzy-turtlebot3-simulations \
    ros-jazzy-turtlebot3-gazebo \
    ros-jazzy-turtlebot3-navigation2 \
    ros-jazzy-nav2-bringup \
    ros-jazzy-nav2-msgs \
    gazebo \
    && rm -rf /var/lib/apt/lists/*

# Set TurtleBot3 model
ENV TURTLEBOT3_MODEL=burger
ENV ROS_DOMAIN_ID=0

# Create workspace
WORKDIR /omokai

# Copy project files
COPY llm_planner.py .
COPY mission_validator.py .
COPY mission_executor.py .
COPY run_mission.py .
COPY omokai.sh .

# Install Python dependencies in venv
RUN python3 -m venv venv && \
    venv/bin/pip install groq pyyaml

# Make launch script executable
RUN chmod +x omokai.sh

# Source ROS in bashrc
RUN echo "source /opt/ros/jazzy/setup.bash" >> /root/.bashrc && \
    echo "export TURTLEBOT3_MODEL=burger" >> /root/.bashrc && \
    echo "alias omokai-mission='cd /omokai && source venv/bin/activate && source /opt/ros/jazzy/setup.bash && python3 run_mission.py'" >> /root/.bashrc

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash"]
