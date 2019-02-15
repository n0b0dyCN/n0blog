title: Sample
summary: A sample markdown file for test.
tags: markdown

# n0blog

Personal blog for those who knowns how to use docker and scp.

This blog is inspired by [phithon's blog](https://www.leavesongs.com/) and [defcon-2018 home page](https://www.oooverflow.io/).

## What we support

1. Adding post in markdown format.
2. Posts content searching.
3. Customized friend links.
4. An easy to use admin panel helping for posts, comments, friend links management and so on.
5. Backup and restore.

## Basic usage

### configure admin password in docker-compose.yml

``` yaml
    - ADMIN_PASS = YOUR_ADMIN_PASSWORD
```

### Run n0blog

``` bash
git clone https://github.com/n0b0dyCN/n0blog.git
cd n0blog
mkdir posts
docker-compose up --build
```

### Add a post

1. Create a folder under `./posts/`. The resources and the markdown file should be in this folder.
2. Create a new file with name `post.md` in the folder you just created.
3. Add meta data for `post.md` with keyword: **title**, **summary** and comma seperated **tags** like:

    ``` markdown
    title: Sample
    summary: A sample markdown file for test.
    tags: markdown,sample
    ```

4. Start your writing in `post.md`
5. Visit `http://your.personal.domain/admin`, enter password you set in `docker-compose.yml`, and set the new post visiable in posts tab.
6. Wait for people reading!

In this repo, we provide a sample post `./posts/sample/`.

#### Note

* All pictures you used in your post should be in the same folder with `post.md`, And you can just use the relative path to insert picture in the markdown file:

``` markdown
![A example picture]("example.png")
```

* For safety reason, static resources reference inside markdown file besides picture is not allowed.

### Add resume

Just add a post with title "resume".

### Backup and restore

The backup is a zip file which contains the posts folder and a `backup.sql` in it.

To backup your data, goto admin panel and select tab `Backup`. Then click the "backup" button to generate a backup file.

To download the newest backup file, click the "download backup" button.

To restore the data, first stop the whole docker compose. Then, unzip the zip file you just downloaded and replace `/posts` the unzipped folder. Finally, restart the docker compose. The script `backup.sql` will be excuted atomatically when n0blog is starting.

## Todo

* [x] Comment showing
* [x] Add post delete function
* [x] Add redis support
* [x] Remove not used libiraries
* [x] Back to top button
* [x] Refactoring function `add_or_update_post`
* [x] Statistics
* [x] Easy backup and restore

# LISENSE
 
The MIT License (MIT)

Copyright (c) 2015 Chris Kibble

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.