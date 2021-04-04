#include "tester.hpp"

#include <iostream>
#include <sstream>

#include <utki/debug.hpp>

#include "util.hxx"

using namespace testy;

void tester::run(){
	// TODO: parallel run
	for(const auto& s : this->suites){
		for(const auto& p : s.second.procedures){
			std::cout << "\e[1;33;4mrun\e[0m " << s.first << ": " << p.first << std::endl;
			try{
				ASSERT(p.second)
				p.second();
				++this->num_passed;
			}catch(testy::check_failed& e){
				++this->num_failed;
				std::stringstream ss;
				ss << "\e[1;31mfailed\e[0m: " << s.first << "/" << p.first << std::endl;
				ss << "  " << e.file << ":" << e.line << ": \e[1;31merror\e[0m: " << e.message;
				std::cout << ss.str() << std::endl;
			}
		}
	}
}

suite& tester::create_suite(const std::string& id){
	validate_id(id);

	auto i = this->suites.emplace(id, suite());
	if(!i.second){
		std::stringstream ss;
		ss << "could not create test suite: suite with id '" << id << "' already exists";
		throw std::invalid_argument(ss.str());
	}
	return i.first->second;
}
