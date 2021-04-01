#include "runner.hpp"

#include <sstream>

using namespace testlord;

void runner::add(const std::string& id, std::function<void()>&& proc){
	auto r = this->procedures.insert(std::make_pair(id, std::move(proc)));
	if(!r.second){
		std::stringstream ss;
		ss << "test with id = " << id << " is already added";
		throw std::invalid_argument(ss.str());
	}
}
