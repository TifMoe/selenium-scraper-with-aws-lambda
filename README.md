# Serverless Scraper in AWS Lambda function

To run a headless browser with Selenium from within a Lambda function, we are going to leverage the [Serverless Framework](https://www.serverless.com/framework/docs/getting-started/)
 to build a layered application with one of the layers containing headless chromium and chromedriver executables.
 
Huge thanks to those that have written about their experience with Selenium + Lambda Layers in [this blog](https://hackernoon.com/running-selenium-and-headless-chrome-on-aws-lambda-layers-python-3-6-bd810503c6c3)!

## Prerequisites
It is incredibly easy for versions of Python, Selenium, Chrome Driver and Chromium to not play well with each other so I ended up
using an older version of Chrome which is known to work with certain versions of Chromium and Selenium:

Dependencies | Version      
--- | --- 
Python | 3.6 
Selenium | 2.7
Chrome Driver | [2.37](https://chromedriver.storage.googleapis.com/2.37/chromedriver_linux64.zip)
Headless Chromium Binary | [1.0.0-41](https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-41/stable-headless-chromium-amazonlinux-2017-03.zip)

Because AWS Lambda functions run in a Linux environment you should make sure your Chromedriver and 
Chromium distributions are compatible (see versions that worked for me above)

## AWS
You obviously need to have an AWS account, preferably with a dedicated IAM user to use in the serverless deployments. 
If you've already installed the [AWS-cli](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html) you 
might want to go ahead and configure your project with a user's Access ID, Secret Key and default region (you can also
do this with the Serverless CLI if you don't already have AWS CLI installed). 


## Serverless Framework
This project leverages the [Serverless Framework](https://www.serverless.com/framework/docs/providers/aws/) to deploy a layered
application via the [CloudFormation stack](https://www.serverless.com/framework/docs/providers/aws/guide/resources/)

You should register for a Serverless account and follow the docs to configure 
their [CLI](https://www.serverless.com/framework/docs/providers/aws/cli-reference/config-credentials/) for your
AWS user.

To install with Node (if you don't already have node, you can find more installation methods [here](https://www.serverless.com/framework/docs/getting-started/)):
```bash
$ npm install -g serverless
```
    
Initial command to walk you through project configuration with prompts:
```bash
$ serverless
```

   
## Build dependencies
Our first job is to bundle all the project dependencies into the first three layers of our application stack. 
These will be uploaded to a unique S3 bucket in your AWS account to be used in the Lambda function (from `/opt/` folder)

#### Python Dependencies (Selenium)
From root, run:
```bash
$ pip install -r requirements.txt -t ./dependencies/selenium/python/lib/python3.6/site-packages 
```

#### Chrome Driver & Headless Chromium
Again, I'm using some older versions here because these package versions need to all be in sync or the program will 
throw `Chrome cannot be reached` errors (that's a Saturday afternoon I won't get back!)

Download Chrome Driver
```bash
$ curl -SL https://chromedriver.storage.googleapis.com/2.37/chromedriver_linux64.zip > ./dependencies/chromedriver/chromedriver.zip
```

Download Headless Chromium binary 
```bash
$ curl -SL https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-41/stable-headless-chromium-amazonlinux-2017-03.zip > ./dependencies/chromedriver/headless-chromium.zip
```

## Deploy
You should deploy the dependencies stack first:

```bash
$ cd ./dependencies 
$ sls deploy
```

Then you can deploy the lambda function with scraper logic
```bash
$ cd ./lambda-scraper
$ sls deploy
```

## Run
To test invoking the function you can use the serverless command:

```bash
$ sls invoke --function scrape
```

# Monitoring
If we've done this right, we should be able to see logs in two places:
- App overview in Serverless account
- Cloudfront logs in AWS

