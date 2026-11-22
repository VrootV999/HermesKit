#pragma once

#include <variant>
#include <memory>
#include <fstream>
#include <string>
#include <optional>
#include <LIEF/Abstract.hpp>

using ProcessResult = std::variant<
    std::unique_ptr<LIEF::Binary>,
    std::ifstream
>;

ProcessResult process_binary(std::string &file, bool specific = false);
std::optional<std::string> analyse_filetype(std::string &file);
std::optional<std::string> analyse_filetype(const LIEF::Binary &binary);
