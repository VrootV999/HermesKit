package cmd

import (
	"github.com/spf13/cobra"
)

var tui = &cobra.Command{Use: "--gui", Short: "Open GUI", Long: `Open GUI version of HermesKit`, Run: startTui,}

func init(){
	rootCmd.AddCommand(tui)
}

func startTui(c *cobra.Command,args []string){

}
