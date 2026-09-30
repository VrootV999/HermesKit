package cmd

import (
	"HermesKit/UI/CLI/colorgen"
	"fmt"
	"os"
	"charm.land/lipgloss/v2"
	"github.com/spf13/cobra"
)


// rootCmd represents the base command when called without any subcommands
var rootCmd = &cobra.Command{
	Use:   "HermesKit",
	Short: "An Evasion Framework for Red Teamers",
	Long: `HermesKit is a modular Red Team framework built for evasion research against modern security systems like AV, EDR, and XDR. It combines source-code obfuscation and binary post-processing to help operators test defensive resilience and simulate advanced adversary tactics across both user and kernel modes`,
	Run: printFunc,
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

// func CreateGradientStyle(color1 string,color2 string) lipgloss.Style{
// 	// color1 := colors[0]
// 	// color2 := colors[1]
// 	s := lipgloss.NewStyle().BorderForegroundBlend(lipgloss.Color(color1),lipgloss.Color(color2))
// 	return s
// }


func printFunc(c *cobra.Command,args []string){
	style1 := lipgloss.NewStyle().
		Bold(true).
		Foreground(lipgloss.Color(colorgen.RandomBrightHex()))

	style2 := lipgloss.NewStyle(). 
		Foreground(lipgloss.Color(colorgen.RandomBrightHex()))

	style3 := lipgloss.NewStyle(). 
		Foreground(lipgloss.Color(colorgen.RandomBrightHex()))

	style4 := lipgloss.NewStyle(). 
		Foreground(lipgloss.Color(colorgen.RandomBrightHex()))
	// color1, color2 := colorgen.GenerateRandomGradientHex()
	// style4 := 	CreateGradientStyle(color1,color2)
	banner := `
	   _    _                              _  ___ _   
	  | |  | |                            | |/ (_) |  
	  | |__| | ___ _ __ _ __ ___   ___ ___| ' / _| |_ 
	  |  __  |/ _ \ '__| '_  _ \ / _ \/ __|  < | | __|
	  | |  | |  __/ |  | | | | | |  __/\__ \ . \| | |_ 
	  |_|  |_|\___|_|  |_| |_| |_|\___||___/_|\_\_|\__|
	`
	banners := style1.Render(banner)
	fmt.Println(banners)

	shortDetail := style3.Render(c.Short)
	fmt.Println("   " + shortDetail)

	longDetail := style4.Render(c.Long)
	fmt.Println(longDetail)

	usages := style2.Render(c.UsageString())
	fmt.Println(usages) 
}
