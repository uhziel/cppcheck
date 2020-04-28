//#include <deque>
//#include <list>

class Foobar
{
public:
	void AddInt(int v) {
		m_int_deque.push_back(v);
	}
	void AddIndex(int index) {
		m_index_list.push_back(index);
	}
	bool IsHaveValue(int v) {
		for (std::list<int>::iterator it = m_index_list.begin();
			it != m_index_list.end(); it++)
		{
			int index = *it;
			if (index < 0 || index >= m_value_deque.size())
			{
				continue;
			}
			if (m_value_deque[index] == v)
			{
				return true;
			}
		}

		return false;
	}
private:
	std::list<int> m_index_list;
	std::deque<int> m_value_deque;
}

int main() {
	Foobar tmp;
	tmp.IsHaveValue(10);
	tmp.AddInt(11);
	return 0;
}
