#include <memory>
#include <fstream>
#include <optional>
#include <iostream>
#include <stdexcept>
#include <variant>
#include <sys/stat.h>
#include <filesystem>

#include "LIEF/ART/utils.hpp"
#include "LIEF/ELF/utils.hpp"
#include "LIEF/MachO/utils.hpp"
#include "LIEF/OAT/utils.hpp"
#include "LIEF/PE/utils.hpp"
#include "LIEF/DEX/utils.hpp"
#include "LIEF/VDEX/utils.hpp"
#include "LIEF/Abstract.hpp"

#include "LIEF/PE/Binary.hpp"
#include "LIEF/ELF/Binary.hpp"
#include "LIEF/MachO/Binary.hpp"

#include "constants.hpp"

using Detector = bool(*)(const std::string&);
using BinaryDetector = bool(*)(const LIEF::Binary*);

//todo: write a datatype conversion function to change LIEF::Binary to its subsequent binary type using dynamic_pointer_cast so that we can do various tasks
static const std::pair<const char*, Detector> checks[7] = {
    {"ELF", LIEF::ELF::is_elf},
    {"ART", LIEF::ART::is_art},
    {"MachO", LIEF::MachO::is_macho},
    {"OAT", LIEF::OAT::is_oat},
    {"VDEX", LIEF::VDEX::is_vdex},
    {"PE", LIEF::PE::is_pe},
    {"DEX", LIEF::DEX::is_dex}
};

static const std::pair<const char*, BinaryDetector> binary_checks[] = {
    {"ELF",   LIEF::ELF::Binary::classof},
    {"PE",    LIEF::PE::Binary::classof},
    {"MachO", LIEF::MachO::Binary::classof}
};

using ProcessResult = std::variant<std::unique_ptr<LIEF::Binary>,std::ifstream,std::nullopt_t>;

std::optional<std::string> analyse_filetype(std::string &file) {
    if (!std::filesystem::exists(file)){
        throw FileNotExist(file);
    }
    for (const auto& [name,detector] : checks){
        if(detector(file)){
            return name;
        }
    }
    return std::nullopt;
}

std::optional<std::string> analyse_filetype(const LIEF::Binary &binary) {
    for (const auto& [name,detector] : binary_checks){
        if (detector(&binary)){
            return name;
        }
    }
    return std::nullopt;
}

ProcessResult process_binary(std::string &file,bool specific=false){
    if (!std::filesystem::exists(file)){
        throw FileNotExist(file);
        return std::nullopt;
    }
    if (specific){
        std::ifstream f(file, std::ios::binary);
        if (!f.is_open()) {
            throw ParseError(file);
        }
        return f;
    }
    auto binary = LIEF::Parser::parse(file);
    if (!binary){
        throw ParseError(file);
        std::cout << "failed to parse" << std::endl;
    }
    for (const auto& section : binary->sections()){
        std::cout << section.name() << std::endl;
    }
    return binary;
}
