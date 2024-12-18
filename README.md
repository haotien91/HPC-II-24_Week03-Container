# Week 3 - Container

## Test Images

### Easy Cases
| ID | Description | URL |
|----|-------------|-----|
| Easy01 | Simple cat portrait | https://files.catbox.moe/hw0iuf.JPG |
| Easy02 | Clear cat photo | https://files.catbox.moe/4z6359.JPG |
| Easy03 | Direct cat shot | https://files.catbox.moe/dspu24.JPG |
| Easy04 | Cat close-up | https://files.catbox.moe/nl2qx8.JPG |
| Easy05 | Clear cat image | https://files.catbox.moe/mck694.JPG |
| Easy06 | Simple cat pose | https://files.catbox.moe/6hoe11.JPG |
| Easy07 | Clear cat view | https://files.catbox.moe/00wbkw.JPG |
| Easy08 | Direct cat image | https://files.catbox.moe/aueojt.jpg |
| Easy09 | Clear cat photo | https://files.catbox.moe/hw8gqz.jpg |
| Easy10 | Simple cat shot | https://files.catbox.moe/ojamnv.png |

### Hard Cases
| ID | Description | URL |
|----|-------------|-----|
| Hard01 | Complex scene | https://files.catbox.moe/972qgb.jpg |
| Hard02 | Multiple objects | https://files.catbox.moe/qd8xcg.jpg |
| Hard03 | Challenging pose | https://files.catbox.moe/5l9n5u.jpg |
| Hard04 | Obscured view | https://files.catbox.moe/sbp9az.jpg |
| Hard05 | Complex background | https://files.catbox.moe/5s6cou.jpg |
| Hard06 | Difficult angle | https://files.catbox.moe/2ib47k.jpg |
| Hard07 | Partial visibility | https://files.catbox.moe/6kbv1w.jpg |
| Hard08 | Complex lighting | https://files.catbox.moe/p5k3vu.jpg |
| Hard09 | Unusual perspective | https://files.catbox.moe/tbgzy0.jpg |
| Hard10 | Challenging environment | https://files.catbox.moe/rz1lp7.jpg |

## Setup Instructions

### Server Part (On Art server)
1. Create & Enter python environment
```bash
conda create -n <ENV_NAME> python=3.10 -y
conda activate <ENV_NAME>
```

2. Clone the repository
```bash
git clone https://github.com/haotien91/HPC-II-24_Week03-Container.git
cd HPC-II-24_Week03-Container
```

3. Install requirement
```bash
pip install -r requirements.txt
```

4. Install support for GroundingDINO
```bash
pip install -e /home/share/MODELS/GroundingDINO
```

5. Create environment file
```bash
# Copy the example file
cp .env.example .env

# Edit the .env file with your student ID
# Example: if your student ID is 111062371
# then PORT=2371
nano .env
```

6. Start the server
```bash
# Make sure you're in the correct environment
conda activate <ENV_NAME>

# Start the server
python server.py
```

7. Verify the server is running
- The server should start without any errors
- You should see a message indicating the server is running on your specified port

8. Then, stop the server with Ctrl-C.


### Local Part (On your computer)

1. Download the client.py file provided on the EECLASS

2. Install required packages
```bash
pip install requests Pillow
```

3. Run the client
```bash
python client.py \
    --model <MODEL_TYPE> \
    --image_url <provided cat pictures> \
    --output <output path> \
    --port <YOUR_PORT>
```

Parameters:
- `--model`: Choose between "DINO" or "YOLO"
- `--image_url`: URL of the image to process (use URLs from the tables above)
- `--output`: Path where the result image will be saved
- `--port`: Your assigned port number (last 4 digits of your student ID)

Example:
```bash
python client.py \
    --model DINO \
    --image_url "https://files.catbox.moe/972qgb.jpg" \
    --output cat_detected.jpg \
    --port 3038
```

## Assignment: Dockerfile

Your task is to create a Dockerfile that containerizes the server application. The Dockerfile should:

1. Use an appropriate base image
2. Install all required dependencies
3. Copy the necessary files
4. Set up the environment
5. Expose the correct port
6. Define the startup command

Requirements:
- The container should be able to access the model files
- The application should be accessible from outside the container
- The container should handle the environment variables properly

Tips:
- Consider using multi-stage builds to reduce image size
- Remember to handle the model file paths correctly
- Think about security best practices
- Consider using environment variables for configuration
- Feel free to use ChatGPT, Claude or Gemini 🥸

## Testing Your Container

After creating your Dockerfile, you can test it with:

```bash
# Build the image
docker build -t <IMAGE_NAME_YOU_WANT> .

# Run the container
docker run -p <YOUR_PORT>:<YOUR_PORT> \
    -v /home/share/MODELS:/home/share/MODELS <IMAGE_NAME_YOU_WANT>
```

| WARNING: please use `docker images` to make sure your image name does not collide with others.


## Submission

Submit the following 2 files on EECLASS:
1. completed Dockerfile
2. PDF report <STUDENT_ID>_container.pdf
    - You must discuss the result of DINO and YOLO model on EASY and HARD cat pictures
    - A screenshot that you do setup an API
    - Include comparison results for both models on selected test cases
        - Which one is better?
        - Why it is better?
