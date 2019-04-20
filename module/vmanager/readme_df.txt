# 一些说明
# 容器中需要安装mysqld，目前没有配置在Dockerfile中，需要手动安装和配置

# 数据库表的生成要使用python命令
# 在manage.py文件目录中运行
# python manage.py migrate
# 有变更时要先运行
# python manage.py makemigrations


# 以下是订阅请求的一个例子
curl -X POST \
  http://localhost:8510/vnfpkgm/v1/subscriptions \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: 526aa5f8-9960-4b3a-baea-37aec362f02b' \
  -H 'cache-control: no-cache' \
  -d '{
	"filter" : {
		"notificationTypes" : ["VnfPackageOnboardingNotification"],
		"vnfProductsFromProviders" : [
			{
				"vnfProvider" : "certus-1",
				"vnfProducts" : [
					{
						"vnfProductName" : "vnfProductName-1",
						"versions" : [
							{
								"vnfSoftwareVersion" : "vnfSoftwareVersion-1",
								"vnfdVersions" : ["vnfdVersions-1"]
							}
						]
					}
				]
			}
		],
		"operationalState" : ["ENABLED"],
		"usageState" : ["IN_USE"]
	},
	"callbackUri" : "http://localhost:8080/mano-vnfm/rest/so/v1/catalog/notification",
	"authentication" : "authentication"
}
'
