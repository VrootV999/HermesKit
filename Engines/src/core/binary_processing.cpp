#include "LIEF/Abstract/Parser.hpp"
#include <memory>
#include <fstream>
#include <optional>
#include <iostream>
#include "LIEF/ART/utils.hpp"
#include "LIEF/ELF/utils.hpp"
#include "LIEF/MachO/utils.hpp"
#include "LIEF/OAT/utils.hpp"
#include "LIEF/PE/utils.hpp"
#include "LIEF/DEX/utils.hpp"
#include "LIEF/VDEX/utils.hpp"
#include "LIEF/Abstract.hpp"
#include <variant>

using Detector = bool(*)(const std::string&);

static const std::pair<const char*, Detector> checks[] = {
    {"ELF", LIEF::ELF::is_elf},
    {"ART", LIEF::ART::is_art},
    {"MachO", LIEF::MachO::is_macho},
    {"OAT", LIEF::OAT::is_oat},
    {"VDEX", LIEF::VDEX::is_vdex},
    {"PE", LIEF::PE::is_pe},
    {"DEX", LIEF::DEX::is_dex}
};

using ProcessResult = std::variant<std::unique_ptr<LIEF::Binary>,std::ifstream>;

std::optional<std::string> analyse_filetype(std::string &file) {
    for (const auto &[name,detector] : checks){
        if (detector(file)){
            return name;
        }
    }
    return std::nullopt;
}

ProcessResult process_binary(std::string &file,bool specific=false){
    if (specific){
        std::ifstream f;
        f.open(file);
        return f;
    }
    // auto btype = analyse_filetype(file);
    auto binary = LIEF::Parser::parse(file);
    if (!binary){
        std::cout << "failed to parse" << std::endl;
    }
    for (const auto& section : binary->sections()){
        std::cout << section.name() << std::endl;
    }
    return binary;
}
