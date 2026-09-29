package cmd

import (
	"os"
	"github.com/spf13/cobra"
)

// rootCmd represents the base command when called without any subcommands
var rootCmd = &cobra.Command{
	Use:   "HermesKit",
	Short: "An Evasion Framework for Red Teamers",
	Long: `HermesKit is a comprehensive, modular Red Team framework engineered for advanced evasion research against modern security solutions, including Antivirus (AV), Endpoint Detection and Response (EDR), and Extended Detection and Response (XDR) systems.

Designed for both source-code obfuscation and binary post-processing, HermesKit provides operators with the tools necessary to test detection engineering resilience, understand defensive blind spots, and simulate sophisticated adversary tactics across user-mode and kernel-mode environments.`,
	// Run: func(cmd *cobra.Command, args []string) { },
}

func Execute() {
	err := rootCmd.Execute()
	if err != nil {
		os.Exit(1)
	}
}

func init() {
	rootCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")
}

