function posts_table_init() {
	var $posts_table = $('#admin-posts-table');
	$posts_table.bootstrapTable({
		url: "/admin/api/getposts",
		methods: "POST",
		contentType: "application/x-www-form-urlencoded",
		dataType: "json",
		striped: true,
		uniqueID: "id",
		showRefresh: true,
		undefinedText: "-",
		sidePagination: "server",
		pageSize: 20,
		pageList: "[10, 20, 50, 80, 100]",
		paginationFirstText: "First Page",
		paginationPreText: "Previous",
		paginationNextText: "Next",
		paginationLastText: "Last Page",
		iconsPrefix: 'iconfont',
		icons: {
			refresh: 'icon-refresh'
		},
		columns: [
			{
				field: 'path',
				title: 'path',
				align: 'center', valign: 'middle'
			}, {
				field: 'title',
				title: 'title',
				align: 'center', valign: 'middle'
			}, {
				field: 'date',
				title: 'date',
				align: 'center', valign: 'middle'
			}, {
				field: 'tags',
				title: 'tags',
				align: 'center', valign: 'middle'
			}, {
				field: 'refresh',
				title: 'refresh',
				align: 'center', valign: 'middle',
				formatter: function (value, row, index, field) {
					var s = '<button class="btn" id="refresh"><i class="iconfont icon-refresh"></i></button>';
					return s;
				},
				events: {
					'click #refresh': function (e, value, row, index) {
						alert("refresh: "+JSON.stringify(row));
						$.post("/admin/api/posts/refresh", {path:row['path']});
						$posts_table.bootstrapTable('refresh');
					}
				}
			}, {
				field: 'show',
				title: 'show',
				align: 'center', valign: 'middle',
				formatter: function (value, row, index, field) {
					var s = '';
					if (value==1) {
						s = '<button class="btn" id="show"><i class="iconfont icon-show"></i></button>';
					} else {
						s = '<button class="btn" id="hide"><i class="iconfont icon-hide"></i></button>';
					}
					return s;
				},
				events: {
					'click #hide': function (e, value, row, index) {
						alert("hide: "+JSON.stringify(row));
						$.post("/admin/api/posts/show", {title:row['title']});
						$posts_table.bootstrapTable('refresh');
					},
					'click #show': function (e, value, row, index) {
						alert("hide: "+JSON.stringify(row));
						$.post("/admin/api/posts/hide", {title:row['title']});
						$posts_table.bootstrapTable('refresh');
					}
				}
			}
		]
	})
};

function links_table_init() {
	var $links_table = $("#admin-links-table");
	$links_table.bootstrapTable({
		url: "/admin/api/links/getlinks",
		methods: "POST",
		contentType: "application/x-www-form-urlencoded",
		dataType: "json",
		striped: true,
		uniqueID: "id",
		showRefresh: true,
		undefinedText: "-",
		sidePagination: "server",
		pageSize: 20,
		pageList: "[10, 20, 50, 80, 100]",
		paginationFirstText: "First Page",
		paginationPreText: "Previous",
		paginationNextText: "Next",
		paginationLastText: "Last Page",
		iconsPrefix: 'iconfont',
		icons: {
			refresh: 'icon-refresh'
		},
		columns: [
			{
				field: 'name',
				title: 'name',
				align: 'center', valign: 'middle'
			}, {
				field: 'link',
				title: 'link',
				align: 'center', valign: 'middle',
				editable: {
					type: 'text',
					title: 'link',
					validate: function (v) {
						if (!v) return 'Link should not be empty';
					}
				}
			}, {
				field: 'description',
				title: 'description',
				align: 'center', valign: 'middle',
				editable: {
					type: 'text',
					title: 'description',
					validate: function (v) {
						if (!v) return 'Description should not be empty';
					}
				}
			}, {
				field: 'action',
				title: 'action',
				align: 'center', valign: 'middle',
				formatter: function (value, row, index, field) {
					s = '';
					s += '<button class="btn mx-1" id="move-up"><i class="iconfont icon-move-up"></i></button>';
					s += '<button class="btn mx-1" id="move-down"><i class="iconfont icon-move-down"></i></button>';
					s += '<button class="btn mx-1" id="delete"><i class="iconfont icon-delete"></i></button>';
					return s;
				},
				events: {
					'click #move-up': function (e, value, row, index) {
						alert("move up");
					},
					'click #move-down': function (e, value, row, index) {
						alert("move down");
					},
					'click #delete': function (e, value, row, index) {
						$.post("/admin/api/links/delete", row, function(){
							$links_table.bootstrapTable('refresh');
						});
					}
				}
			}
		],
		onEditableSave: function (field, row, oldValue, $el) {
			$.post("/admin/api/links/update", row, function(){
				$links_table.bootstrapTable('refresh');
			});
		}
	})
};


function comments_table_init() {
	var $comments_table = $("#admin-comments-table");
	$comments_table.bootstrapTable({
		url: "/admin/api/comments/getcomments",
		methods: "POST",
		contentType: "application/x-www-form-urlencoded",
		dataType: "json",
		striped: true,
		uniqueID: "id",
		showRefresh: true,
		undefinedText: "-",
		sidePagination: "server",
		pageSize: 20,
		pageList: "[10, 20, 50, 80, 100]",
		paginationFirstText: "First Page",
		paginationPreText: "Previous",
		paginationNextText: "Next",
		paginationLastText: "Last Page",
		iconsPrefix: 'iconfont',
		icons: {
			refresh: 'icon-refresh'
		},
		columns: [
			{
				field: 'post_title',
				title: 'post',
				align: 'center', valign: 'middle'
			}, {
				field: 'name',
				title: 'name',
				align: 'center', valign: 'middle',
				formatter: function(value, row, index, field) {
					s = '';
					s += '<a href="' + row['url'] + '">' + value + '</a>';
					s += '<p>' + row['email'] + '</p>';
					return s;
				}
			}, {
				field: 'time',
				title: 'time',
				align: 'center', valign: 'middle'
			}, {
				field: 'content',
				title: 'content',
				align: 'center', valign: 'middle'
			}, {
				field: 'show',
				title: 'action',
				align: 'center', valign: 'middle',
				formatter: function(value, row, index, field) {
					s = '';
					if (value == true) {
						s += '<button class="btn mx-1" id="show"><i class="iconfont icon-show"></i></button>';
					} else {
						s += '<button class="btn mx-1" id="hide"><i class="iconfont icon-hide"></i></button>';
					}
					s += '<button class="btn mx-1" id="delete"><i class="iconfont icon-delete"></i></button>';
					return s;
				},
				events: {
					'click #show': function(e, value, row, index) {
						$.post('/admin/api/comments/hide', row, function(){
							$comments_table.bootstrapTable('refresh');
						});
					},
					'click #hide': function(e, value, row, index) {
						$.post('/admin/api/comments/show', row, function(){
							$comments_table.bootstrapTable('refresh');
						});
					},
					'click #delete': function(e, value, row, index) {
						$.post('/admin/api/comments/delete', row, function(){
							$comments_table.bootstrapTable('refresh');
						});
					}
				}
			}
		]
	})
};

function init_links_add_table() {
	$("#link-add-form").submit(function(event){
		event.preventDefault();
		var form = $(this);
		console.log(form.serialize());
		$.ajax({
			type: form.attr('method'),
			url: form.attr('action'),
			data: form.serialize(),
			success: function(){
				$("#admin-links-table").bootstrapTable('refresh');
			}
		});
	})
}

posts_table_init();
links_table_init();
comments_table_init();
init_links_add_table();
