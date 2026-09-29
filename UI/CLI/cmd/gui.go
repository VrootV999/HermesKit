package cmd

import (
	"github.com/spf13/cobra"
)

var gui = &cobra.Command{Use: "--gui", Short: "Open GUI", Long: `Open GUI version of HermesKit`, Run: startGui,}

func init(){
	rootCmd.AddCommand(gui)
}

func startGui(c *cobra.Command,args []string){

}
