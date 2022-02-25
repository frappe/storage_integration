<div align="center">
    <img src="https://frappecloud.com/files/6.png" style="height:128px;border-radius:25px;">
    <h2>S3 Storage Integration</h2>
</div>

S3 Storage Integration for Frappe Cloud, that stores everything including backups on s3

#### Features
1. Direct uploads to s3 (no middlewares)
2. Migrate existing data from site to s3
3. Restore data from s3 to site
4. Clean data from site or s3
5. Store all backups on s3, including database backups (WIP)
6. Usage Analytics (WIP)
6. Built using [Minio](https://min.io/) and [AWS S3](https://aws.amazon.com/s3/)

#### Installation
* Frappe Cloud users can install it from [Marketplace](https://frappecloud.com/marketplace/apps/storage_integration)
* After installing you will get all the keys via email. These keys will give you access to all of your resources stored on s3, so don't share it with anyone unless necessary.
* Add the keys in the doctype below
<img width="1376" alt="Screenshot 2022-02-25 at 5 37 43 PM" src="https://user-images.githubusercontent.com/50401596/155713102-22415afd-6775-4034-89f5-d32583050e01.png">

#### License

MIT
