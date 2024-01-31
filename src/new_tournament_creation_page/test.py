from copy import deepcopy
from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        current_node_of_result = ListNode()
        head_of_result = current_node_of_result
        l1_current = l1
        l2_current = l2
        flag = 0

        while True:

            if l1_current is None and l2_current is None:
                current_node_of_result.val = 1
                break

            elif l1_current is None:
                current_node_of_result.val = (l2_current.val + flag) % 10
                flag = (l2_current.val + flag) // 10

                if l2_current.next is None:
                    if flag == 0:
                        break

                l2_current = l2_current.next
                current_node_of_result.next = ListNode()
                current_node_of_result = current_node_of_result.next

            elif l2_current is None:
                current_node_of_result.val = (l1_current.val + flag) % 10
                flag = (l1_current.val + flag) // 10

                if l1_current.next is None:
                    if flag == 0:
                        break

                l1_current = l1_current.next
                current_node_of_result.next = ListNode()
                current_node_of_result = current_node_of_result.next

            else:
                value = l1_current.val + l2_current.val + flag
                current_node_of_result.val = value % 10
                flag = value // 10

                if l1_current.next is None and l2_current.next is None:
                    if flag == 0:
                        break

                l1_current = l1_current.next
                l2_current = l2_current.next
                current_node_of_result.next = ListNode()
                current_node_of_result = current_node_of_result.next

        return head_of_result


solution = Solution()
print(solution.addTwoNumbers(ListNode(2, ListNode(4, ListNode(3, None))),
                             ListNode(2, ListNode(4, ListNode(3, None)))))
