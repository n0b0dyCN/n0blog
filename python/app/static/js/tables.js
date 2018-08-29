function posts_table_init() {
	var $posts_table = $('#admin-posts-table');
	$posts_table.bootstrapTable({
		url: "/admin/getposts",
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
						$.post("/admin/posts/refresh", {title:row['title']});
					}
				}
			}, {
				field: 'show',
				title: 'show',
				align: 'center', valign: 'middle',
				formatter: function (value, row, index, field) {
					var s = '';
					if (value==1) {
						s = '<button class="btn" id="hide"><i class="iconfont icon-hide"></i></button>';
					} else {
						s = '<button class="btn" id="show"><i class="iconfont icon-show"></i></button>';
					}
					return s;
				},
				events: {
					'click #hide': function (e, value, row, index) {
						alert("hide: "+JSON.stringify(row));
						$.post("/admin/posts/hide", {title:row['title']});
					},
					'click #show': function (e, value, row, index) {
						alert("hide: "+JSON.stringify(row));
						$.post("/admin/posts/show", {title:row['title']});
					}
				}
			}
		]
	})
};

posts_table_init();
