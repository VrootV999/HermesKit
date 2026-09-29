package cmd

import (
	"github.com/spf13/cobra"
)

var tui = &cobra.Command{Use: "--tui", Short: "TUI HermesKit", Long: `Open TUI version of HermesKit`, Run: startTui,}

func init(){
	rootCmd.AddCommand(tui)
}

func startTui(c *cobra.Command,args []string){

}
