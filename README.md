### Background
- A newly established e-commerce company has high traffic but a low web-to-purchase conversion rate. Therefore, we predict the likelihood of each user making a purchase and implement targeted discount policies to encourage them to buy.

### Achievements
- RFM Analysis: Conducted detailed RFM (Recency, Frequency, Monetary) analysis to classify users based on their purchasing behavior.
- Purchase Propensity Model: Used a propensity model to forecast user behavior and identify individuals who need encouragement to make a purchase.

---

## Run Docker
Ensure that Docker is installed on your machine. Check by running:

```bash
docker --version
```

### Step 1: Build Docker Image

Navigate to the directory containing the Dockerfile for the Customer-propensity-to-purchase application:

```bash
cd Customer-propensity-to-purchase
```

Build the Docker image from the Dockerfile:

```bash
docker build -t customer-propensity-to-purchase .
```

### Step 2: Run the Customer-propensity-to-purchase Application

Run the Customer-propensity-to-purchase application in a Docker container:

```bash
docker run -p 8000:8000 customer-propensity-to-purchase
```

The application will run and listen on port 8000.

### Step 3: Log in to Docker Hub

Log in to Docker Hub from the terminal:

```bash
docker login
```

Enter your username and password when prompted.

### Step 4: Tag and Push Docker Image to Docker Hub

Tag your Docker image with the repository name on Docker Hub:

```bash
docker tag customer-propensity-to-purchase:latest diends/yourname:image_name
```

Push the Docker image to Docker Hub:

```bash
docker push diends/yourname:image_name
```

### Step 5: Run Application from Docker Hub

Now, you can run the backend application from the image pushed to Docker Hub:

```bash
docker run -it --name customer-propensity-to-purchase -p 8000:8000 diends/yourname:image_name
```

---

Make sure to replace `diends` with your Docker Hub username and `yourname` with your application/yourname.
