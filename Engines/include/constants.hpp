#pragma once

#include <string>
#include <string_view>
#include <stdexcept>
#include <unordered_set>
#include <unordered_map>
#include <array>
#include <vector>
#include <cstdint>

namespace Sections {

    // Packer section names
    inline const std::array<std::unordered_set<std::string>, 3> SECTIONS = {{
        {"UPX0", "UPX1", "UPX2"},
        {"MPRESS1", "MPRESS2"},
        {"ASPack", ".themida", "Themida"}
    }};

    // PE sections
    inline const std::unordered_map<std::string, std::string> PE_SECTIONS = {
        {".text",   "CNT_CODE,MEM_EXECUTE,MEM_READ"},
        {".data",   "CNT_INITIALIZED_DATA,MEM_READ,MEM_WRITE"},
        {".rdata",  "CNT_INITIALIZED_DATA,MEM_READ"},
        {".bss",    "CNT_UNINITIALIZED_DATA,MEM_READ,MEM_WRITE"},
        {".rsrc",   "CNT_INITIALIZED_DATA,MEM_READ"},
        {".reloc",  "CNT_INITIALIZED_DATA,MEM_READ"},
        {".idata",  "CNT_INITIALIZED_DATA,MEM_READ"},
        {".edata",  "CNT_INITIALIZED_DATA,MEM_READ"},
        {".tls",    "CNT_INITIALIZED_DATA,MEM_READ,MEM_WRITE"},
        {".pdata",  "CNT_INITIALIZED_DATA,MEM_READ"}
    };

    // Go sections
    inline const std::unordered_map<std::string, std::string> GO_SECTIONS = {
        {".typelink",      "CNT_INITIALIZED_DATA,MEM_READ"},
        {".itablink",      "CNT_INITIALIZED_DATA,MEM_READ"},
        {".go.buildinfo",  "CNT_INITIALIZED_DATA,MEM_READ"},
        {"CODE",           "CNT_CODE,MEM_EXECUTE,MEM_READ"},
        {"DATA",           "CNT_INITIALIZED_DATA,MEM_READ,MEM_WRITE"},
        {"BSS",            "CNT_UNINITIALIZED_DATA,MEM_READ,MEM_WRITE"}
    };

    // Mach-O segments
    inline const std::unordered_set<std::string> MACHO_SEGMENTS = {
        "__TEXT", "__DATA", "__DATA_CONST", "__LINKEDIT",
        "__OBJC", "__AUTH", "__AUTH_CONST", "__PAGEZERO",
        "__DWARF", "__LLVM", "__RESTRICT", "__INFO_FILTER",
        "__CTF", "__UNICODE"
    };

    // Mach-O sections
    inline const std::unordered_set<std::string> MACHO_SECTIONS = {
        "__text", "__stubs", "__stub_helper", "__cstring",
        "__const", "__data", "__bss", "__common",
        "__literal4", "__literal8", "__literal16",
        "__objc_classlist", "__objc_catlist",
        "__objc_methname", "__objc_methtype",
        "__objc_selrefs", "__objc_classrefs",
        "__objc_const", "__objc_data", "__cfstring",
        "__mod_init_func", "__mod_term_func",
        "__unwind_info", "__eh_frame", "__got",
        "__la_symbol_ptr", "__nl_symbol_ptr",
        "__compact_unwind"
    };

}

class BinaryErrors : public std::runtime_error {
    public:
        using std::runtime_error::runtime_error;
};


// Unknown binary format
class UnknownBinary : public BinaryErrors {
    private:
        std::string bname_;
        std::string btype_;

    public:
        UnknownBinary(const std::string& message,const std::string& bname,const std::string& btype);
        const std::string& bname() const noexcept;
        const std::string& btype() const noexcept;
        const char* what() const noexcept override;
        std::string details() const;

};


// No suitable section
class NoSuitableSection : public BinaryErrors {
    private:
        std::string bname_;
        std::string btype_;

    public:
        NoSuitableSection(const std::string& message,const std::string& bname,const std::string& btype);
        const std::string& bname() const noexcept;
        const std::string& btype() const noexcept;
        std::string details() const;
};


// Binary parsing error
class ParseError : public BinaryErrors {
    private:
        std::string bname_;

    public:
        explicit ParseError(const std::string& binary);
        const std::string& bname() const noexcept;
};

// File isn't available(I personally hate the std::filesystem::filesystem::error) A simpler version for our program
class FileNotExist : public BinaryErrors {
    private: 
        std::string bname_;
    public:
        explicit FileNotExist(const std::string& binary);
        const std::string& bname() const noexcept;

};
// Section does not Exist
class SectionNotFound: public BinaryErrors {
    private: 
        std::string section_;
    public:
        explicit SectionNotFound(const std::string& section);
        const std::string& section() const noexcept;

};
// Improper argument
class ImproperArgument : public BinaryErrors {
    private:
        std::string context_;
        std::string req_;
        std::string val_;

    public:
        ImproperArgument(const std::string& context,const std::string& req,const std::string& val);
        const std::string& context() const noexcept ;
        const std::string& req() const noexcept;
        const std::string& val() const noexcept;
        std::string details() const;
};

template <typename Container>
auto get_random(const Container& container);
std::vector<uint8_t> generateRandomBytes(size_t length = 800);
