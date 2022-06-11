/*
Copyright © 2022 NAME HERE <EMAIL ADDRESS>

*/
package cmd

import (
	"fmt"
	"github.com/sirupsen/logrus"
	"github.com/smurfless1/fancyrun"
	"github.com/smurfless1/gitlike/repo"
	"github.com/smurfless1/pathlib"
	"os"
	"strings"
	"time"

	"github.com/spf13/cobra"
)

var username string
var jira string
var noDate bool

func runBranch(cmd *cobra.Command, args []string) {
	// reduce noise
	logrus.SetLevel(logrus.ErrorLevel)
	branch := strings.Join(args, "-")
	logrus.Info(fmt.Sprintf("creating branch named %s", branch))

	currentTime := time.Now()
	username := os.Getenv("USER")
	cleaned := fmt.Sprintf("%s/%s/%d-%02d-%02d-%s",
		username, jira,
		currentTime.Year(), currentTime.Month(), currentTime.Day(),
		strings.Join(args, "-"))

	if noDate == true {
		cleaned = fmt.Sprintf("%s/%s/%s",
			username, jira, strings.Join(args, "-"))
	}

	rep := repo.New("remote", pathlib.New(""), "main")
	err := rep.SetBranch(cleaned)
	fancyrun.CheckInline(err)

	fmt.Println(fmt.Sprintf("Checked out %s", cleaned))
}

// rootCmd represents the base command when called without any subcommands
var rootCmd = &cobra.Command{
	Use:   "mkbranch",
	Short: "Jira-Name-Friendly Branch Utility",
	Long: `Jira-Name-Friendly Branch Utility

For instance, who remembers the format of the branches, 
or when you created them?

I do.
`,
	Args: cobra.MinimumNArgs(1),
	// Uncomment the following line if your bare application
	// has an action associated with it:
	Run: runBranch,
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

	// Cobra also supports local flags, which will only run
	// when this action is called directly.
	rootCmd.Flags().BoolVar(&noDate, "no-date", false, "do not add date to branch name")
	rootCmd.Flags().StringVar(&username, "username", os.Getenv("USER"), "username to use")
	rootCmd.Flags().StringVar(&jira, "jira", "NO-JIRA", "Which Jira it applies to")
}
