#include <LIEF/Abstract/Header.hpp>
#include <LIEF/Abstract.hpp>

#include <LIEF/MachO/Binary.hpp>
#include <LIEF/PE/Section.hpp>
#include <LIEF/ELF/Section.hpp>
#include <LIEF/MachO/Section.hpp>

#include <LIEF/PE/Builder.hpp>
#include <memory>
#include <optional>
#include <fstream>
#include <random>
#include <string>
#include <algorithm>
#include <cstdlib>
#include <cstdint>
#include <vector>
#include <iostream>
#include <filesystem>
#include <limits>
#include <array>
#include <variant>

#include "constants.hpp"
#include "binary_processing.hpp"

using NullStr = std::optional<std::string>;
using BinType = std::unique_ptr<LIEF::Binary>; 

void mask_sections(BinType &binary,std::string location,NullStr target,NullStr newname,bool evth=false){
    if(!evth){
        if(target.has_value()){
            std::cout << "Target " << static_cast<std::string>(*target) << "\n";
            // looks like iteration is best solution for multi binary checking
            auto ftype = analyse_filetype(binary);
            if (ftype.has_value()){
                auto spectype_binary = std::dynamic_pointer_cast<LIEF::ftype::Binary>
            }
            //todo: use .sections and then loop through them all and see if it has the specific section
            if (binary->has_section(target)){
                std::cout << "No Target Section " << static_cast<std::string>(*target) << "detected \n";
                throw SectionNotFound(target.value());
            };
            //todo: use .sections and then loop through them all and get the specific section and get the every data of the section from it
            auto section = binary->get_section(target);
            if (section == nullptr){
                std::cout << "Invalid Section " << static_cast<std::string>(*target) <<  "\n";
            }else {
                if (newname.has_value()){
                    std::cout << "Masking " << static_cast<std::string>(*target) << "to " << static_cast<std::string>(*newname);
                    section.name = static_cast<std::string>(*newname);
                }else{
                    auto name = get_random(BinarySections::SAFE_SECTIONS);
                    std::cout << "Masking " << static_cast<std::string>(*target) << "to " << name;
                    section.name = static_cast<std::string>(*name);
                }
            };
        }else{
            std::cout << "Masking Section Name\n";
            for (auto section: binary->sections){
                for (auto iter : BinarySections::SECTIONS){
                    if (iter.contains(section.name)){
                        std::cout << "Maskable Section Detected: " << section.name << "@ " << section.virtual_address;
                        auto random_name = get_random(BinarySections::SAFE_SECTIONS);
                        section.name = random_name;
                        std::cout << "Masked Section name with " << random_name;
                    };
                }
            }
        };
    }else{
        for(const auto section: binary.sections){
            section.name = get_random(BinarySections::SAFE_SECTIONS);
        }
    };
    binary->write(location);
    std::cout << "Saved as " << location << "\n";
};

void custom_section(LIEF::Binary &binary,std::string &location,NullStr &name,std::optional<std::vector<uint8_t>> &data){
    std::string section_name = name.has_value() ? name.value() : get_random(BinarySections::SAFE_SECTIONS);
    std::optional<std::string> ftype = analyse_filetype(binary);
    if (ftype.has_value()){
        if(ftype.value() == "PE"){
            auto custom = LIEF::PE::Section(name.value());
            custom.content = (data.has_value()) ? data.value() : generateRandomBytes();
            //todo: call the convertion to get the converted binary type and then call add_section
            binary.add_section(custom);
        }else if(ftype.value() == "ELF"){
            auto custom = LIEF::ELF::Section(name.value());
            custom.content = (data.has_value()) ? data.value() : generateRandomBytes();
            //todo: call the convertion to get the converted binary type and then call add_section
            binary.add(custom);
        }else if(ftype.value() == "MachO"){
            auto custom = LIEF::MachO::Section(name.value());
            custom.content = (data.has_value()) ? data.value() : generateRandomBytes();
            //todo: call the convertion to get the converted binary type and then call add_section
            binary.add_section(custom);
        }
    }
    binary->write(location);
};
void binary_bloater(std::string binary,std::string location,std::optional<int> size){
    std::cout << "Bloating Binary\n";
    auto bin = process_binary(binary,true);
    auto *src = std::get_if<std::ifstream>(&bin);
    if (src == nullptr || !src->is_open()){
        throw ParseError(bin);
    }
    std::ofstream target(location,std::ios::binary); 
    if (!target.is_open()){
        throw ParseError(location);
    }
    if (!size.has_value()) {
        std::vector<uint8_t> data(static_cast<int>(*size) * 1024 * 1024);

        std::generate(data.begin(), data.end(), [] {
            return static_cast<uint8_t>(std::rand() % 256);
        });

        if (auto* stream = std::get_if<std::ifstream>(&bin)) {
            target.write(data.data(), data.size());
        }
    } else {
        std::vector<uint8_t> data(12 * 1024 * 1024);

        std::generate(data.begin(), data.end(), [] {
            return static_cast<uint8_t>(std::rand() % 256);
        });

        if (auto* stream = std::get_if<std::ifstream>(&bin)) {
            target.write(data.data(), data.size());
        }
    }
    target.close();
};

