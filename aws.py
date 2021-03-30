import os

print('''

1. Creating the high availability cluster by just one click in python by automation


''')

os.system("aws configure")

#create key-value pair
os.system("aws ec2 create-key-pair --key-name aws4 --query \"KeyMaterial\"  --output text  >  aws4.pem" )

#creating the security group
sg=input("Enter your sg name:")
os.system("aws ec2 create-security-group --group-name {} --description \"My Security Group\" ".format(sg))

#authorizing the security group for ingress rules
sg_id=input(":Enter security group id:")
os.system("aws ec2 authorize-security-group-ingress --group-id {} --protocol all --cidr 0.0.0.0/0".format(sg_id))

#launching the instance
image_id=input("Enter the image id:")
inst_type=input("Enter instance type")
os.system("aws ec2 run-instances --image-id  {} --instance-type {} --key-name aws4 --security-group-ids {} --placement AvailabilityZone=\"ap-south-1a\" ".format(image_id,inst_type,sg_id))
#print("Instance Launched")

#creating the EBS volume
os.system("aws ec2 create-volume --size 1 --availability-zone ap-south-1a")

#Attaching the EBS to the instance launched
vol_id=input("Enter volume id")
inst_id=input("Enter instance id")
os.system("aws ec2 attach-volume --volume-id {} --instance-id {} --device /dev/sdx".format(vol_id,inst_id))



#creating the S3 bucket
os.system("aws s3 mb s3://task6awscli --region ap-south-1")

#ceating a object and uploading the image 
os.system("aws s3 cp .  s3://task6awscli --recursive --exclude \"*\" --include \"*.svg\"  --acl public-read ")

#creating a cloudfront
os.system("aws cloudfront create-distribution --origin-domain-name task6awscli.s3.amazonaws.com")

#take the cloud front url
cfurl=input("Enter cloudfront url:")


#changing the permission of private key file
os.system("chmod 400 aws4.pem")

#Installing the httpd package by going inside the instance
ip=input("Enter ip")
os.system("ssh -i \"aws4.pem\" ec2-user@{}.ap-south-1.compute.amazonaws.com sudo yum install httpd".format(ip))

#To see all the available hard disks(volumes)
os.system("ssh -i \"aws4.pem\" ec2-user@{}.ap-south-1.compute.amazonaws.com sudo fdisk -l".format(ip))

#format the new volume added
format=input("Enter the name of disk you need to format")
os.system("ssh -i \"aws4.pem\" ec2-user@{}.ap-south-1.compute.amazonaws.com sudo mkfs.ext4 {}".format(ip,format))

#create partition
os.system("ssh -i \"aws4.pem\" ec2-user@{}.ap-south-1.compute.amazonaws.com sudo fdisk {}".format(ip,format))

#format the new partition created

part=input("Enter the block name of new partition created")
os.system("ssh -i \"aws4.pem\" ec2-user@{}.ap-south-1.compute.amazonaws.com sudo mkfs.ext4 {}".format(ip,part))

#mount the partition on /var/www/html folder
os.system("ssh -i \"aws4.pem\" ec2-user@{}.ap-south-1.compute.amazonaws.com sudo mount {} /var/www/html".format(ip,part))

#creating the index.html file
os.system("ssh -i \"aws4.pem\" ec2-user@{}.ap-south-1.compute.amazonaws.com sudo vi /var/www/html/index.html".format(ip))

