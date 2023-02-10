/*
Copyright © 2022 shih <shih@knownsec.com>
*/
package cmd

import (
	"encoding/json"
	"fmt"
	"io/fs"
	"os"
	"path/filepath"
	"runtime"
	"strings"

	"github.com/sourcegraph/conc/pool"
	"github.com/spf13/cobra"
	ffmpeg "github.com/u2takey/ffmpeg-go"
)

var (
	audoDst            string
	dirName            string
	isRepairFileName   bool
	onlyRepairFileName bool
)

func repairName(oldName string) string {
	bname := filepath.Base(oldName)
	ext := filepath.Ext(bname)
	tname := strings.TrimSpace(fileNameWithoutExtTrimSuffix(bname))

	invalidChars := []byte{'\\', '/', ':', '*', '?', '"', '<', '>', '|'}
	for _, c := range invalidChars {
		tname = strings.ReplaceAll(tname, string(c), "")
	}

	return tname + ext
}

func fileNameWithoutExtTrimSuffix(fileName string) string {
	return strings.TrimSuffix(fileName, filepath.Ext(fileName))
}

func doRepaireFileName(fname string) {
	bname := filepath.Base(fname)
	dname := filepath.Dir(fname)
	nname := filepath.Join(dname, repairName(bname))
	if bname != nname {
		os.Rename(fname, nname)
	}
}

func doConvFunction(fname string) {
	data, err := ffmpeg.Probe(fname)
	if err != nil {
		return
	}

	type AudioInfo struct {
		Format struct {
			FormatName string `json:"format_name"`
		} `json:"format"`
	}
	vInfo := &AudioInfo{}
	err = json.Unmarshal([]byte(data), vInfo)
	if err != nil {
		fmt.Println("file:", fname, "info unmarshal err:", err)
		return
	}

	if vInfo.Format.FormatName == audoDst {
		return
	}

	bname := filepath.Base(fname)
	if isRepairFileName {
		bname = repairName(bname)
	}
	dname := filepath.Dir(fname)
	withoutExtName := fileNameWithoutExtTrimSuffix(bname)
	nname := withoutExtName + "." + audoDst
	npath := filepath.Join(dname, nname)
	if err := ffmpeg.Input(fname).Audio().Output(npath, ffmpeg.KwArgs{"format": audoDst}).OverWriteOutput().Run(); err != nil {
		fmt.Println("conv:", fname, "to", npath, "err:", err)
	}
}

// rootCmd represents the base command when called without any subcommands
var rootCmd = &cobra.Command{
	Use:   "conv-audio",
	Short: "conv audio fmt",
	// Uncomment the following line if your bare application
	// has an action associated with it:
	Run: func(cmd *cobra.Command, args []string) {
		p := pool.New().WithMaxGoroutines(runtime.NumCPU())
		filepath.Walk(dirName, func(path string, info fs.FileInfo, err error) error {
			if info.IsDir() {
				return nil
			}

			if onlyRepairFileName {
				p.Go(func() {
					doRepaireFileName(path)
				})
			} else {
				p.Go(func() {
					doConvFunction(path)
				})
			}
			return nil
		})
	},
}

// Execute adds all child commands to the root command and sets flags appropriately.
// This is called by main.main(). It only needs to happen once to the rootCmd.
func Execute() {
	err := rootCmd.Execute()
	if err != nil {
		os.Exit(1)
	}
}

func init() {
	// Here you will define your flags and configuration settings.
	// Cobra supports persistent flags, which, if defined here,
	// will be global for your application.

	// rootCmd.PersistentFlags().StringVar(&cfgFile, "config", "", "config file (default is $HOME/.conv-audio.yaml)")

	// Cobra also supports local flags, which will only run
	// when this action is called directly.
	rootCmd.Flags().StringVarP(&audoDst, "fmt", "f", "mp3", "dest format: default mp3")
	rootCmd.Flags().StringVarP(&dirName, "dir", "d", "", "dir path")
	rootCmd.Flags().BoolVarP(&isRepairFileName, "repair", "r", true, "repair file name")
	rootCmd.Flags().BoolVarP(&onlyRepairFileName, "repair_name", "R", false, "repair file name(only)")
	_ = rootCmd.MarkFlagRequired("dir")
}
