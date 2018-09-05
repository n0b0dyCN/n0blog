# n0blog

Personal blog for those who knowns how to use docker and scp.

## Basic usage:

### configure admin password in docker-compose.yml
```
	- ADMIN_PASS = YOUR_ADMIN_PASSWORD
```

### Run n0blog
```
git clone https://github.com/n0b0dyCN/n0blog.git
cd n0blog
docker-compose up --build
```

### Add a post

1. Make a new directory for a new post.
2. Get into the new directory
3. Create a new file with name `post.md`
4. Start your writing in `post.md`
5. Visit `http://your.personal.domain/admin`, enter password you set in `docker-compose.yml`, and set the new post visiable in posts tab.
6. Wait for people reading!

#### Note:
* All pictures you used in your post should be in the same folder with `post.md`, And you can just use the relative path to insert picture in the markdown file:
``` markdown
![A example picture]("example.png")
```
* For safety reason, static resources reference inside markdown file besides picture is not allowed.

## Todo
- [ ] Add nginx support
- [ ] Add post delete function
- [ ] Add redis support
- [ ] Remove not used libiraries.
