package main

import (
	"flag"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/myZinx/utils"
	"github.com/myZinx/znet"
	"github.com/sirupsen/logrus"
)

var (
	// 单机测试时这仨参数不用传。实际使用时必须传
	datanetServerIp = flag.String("sdip", utils.GlobalObj.LocalServerIp, "server datanet IP")
	ctrlnetServerIp = flag.String("scip", utils.GlobalObj.LocalServerIp, "server ctrlnet IP")
	serverName      = flag.String("sname", utils.GlobalObj.Name, "server Name")
)

// 基于 zinx开发的服务器端应用程序
func main() {
	flag.Parse()
	// logrus.SetLevel(logrus.WarnLevel)
	logrus.SetLevel(logrus.InfoLevel)
	// logrus.SetLevel(logrus.DebugLevel) // 测试的时候只开几个client，就用debug
	log.SetPrefix("[服务端]：")
	now := time.Now() // 只记录每天的日志得了
	logfile, err := os.OpenFile(fmt.Sprintf("log/%s_%s.log", *serverName, now.Format("060102")), os.O_CREATE|os.O_WRONLY|os.O_TRUNC, 0666)
	if err != nil {
		logrus.Fatalf("create or open log file failed: %v", err)
	}
	defer logfile.Close()
	logrus.SetOutput(logfile)
	// 1 创建一个server 句柄，使用 zinx 的api
	s := znet.NewServer(*serverName, *datanetServerIp)
	logrus.Infof("开启百万级连接server，监听地址：%s:%d", s.IP, s.Port)
	go startGin(s)
	s.Serve()
}

// 开一个 gin 服务器去等待命令去开启或关闭 文件请求
func startGin(s *znet.Server) {
	addr := fmt.Sprintf("%s:%d", *ctrlnetServerIp, utils.GlobalObj.ServerGinPort)
	logrus.Infof("开启 控制文件传输的 web 接口，监听地址：%s", addr)
	// 创建一个默认路由
	r := gin.Default()
	gin.SetMode(gin.ReleaseMode)
	r.GET("/StartFileReq", func(ctx *gin.Context) {
		s.AllowFileReq = true
		logrus.Infof(" [GIN] 服务器 %s 收到【开启】文件传输的命令！", *serverName)
		ctx.JSON(http.StatusOK, gin.H{
			"err": "",
		})
	})
	r.GET("/StopFileReq", func(ctx *gin.Context) {
		s.AllowFileReq = false
		logrus.Infof(" [GIN] 服务器 %s 收到【停止】文件传输的命令！", *serverName)
		ctx.JSON(http.StatusOK, gin.H{
			"err": "",
		})
	})
	r.GET("/queryAmountOfConns", func(ctx *gin.Context) {
		logrus.Infof(" [GIN] 服务器 %s 收到【查询】总连接数的命令！", *serverName)
		ctx.JSON(http.StatusOK, gin.H{
			"amountOfConns": s.ConnMgr.GetAmountOfConns(),
		})
	})
	r.Run(addr)
}
